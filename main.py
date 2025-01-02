from input_manager import *
from command_prompt import CommandPrompt
from local import Local
from pyperclip import paste
from renderer import Renderer
from rightclick import RightClickAction
from settings import Settings
from state_master import StateMaster
from text_manager import LineManager, Cursor
from widget import *

"""
from profilehooks import profile
@profile(stdout=False, filename='basic.prof')  # <== Profiling
"""
def main():
    settings = Settings()
    renderer = Renderer(settings)
    line_manager = LineManager()
    renderer.line_manager = line_manager
    input_manager = InputManager()
    state_master = StateMaster(settings)
    local = Local()
    cursor = Cursor(line_manager, settings)

    console = CommandPrompt(line_manager, settings, cursor, renderer, state_master)
    rightclickaction = RightClickAction(renderer, cursor)

    can_update = True
    app_running = True
    macro_mode = False
    widget_manager = WidgetMaster([
        ScrollBar(settings.SCREEN_DIMS[0] - 20, 0, 20, 100, "vertical", settings),
        ScrollBar(0, settings.SCREEN_DIMS[1] - 20, 100, 20, "horizontal", settings)
        ])
    outside_event = None

    while app_running:

        scrollbar_update = False
        event = input_manager.get_pg_events()
        if event in input_manager.REQUIRE_WAIT:
            if state_master.check_is_key_accessible(event):
                can_update = True
            else:
                can_update = False
        force_event = False
        
        if outside_event:
            event = outside_event
            force_event = True
            outside_event = None

        will_update = can_update or force_event
    
        leftclick = True if event == LEFTCLICK else False
        widget_manager.scrollbars_updates(input_manager.get_mouse_pos(), leftclick)
        if widget_manager.mouse_on_widget:
            if widget_manager.focused_widget:
                renderer.set_mouse_nature(pg.SYSTEM_CURSOR_HAND)
            else:
                renderer.set_mouse_nature(pg.SYSTEM_CURSOR_ARROW)
        else:
            renderer.set_mouse_nature(pg.SYSTEM_CURSOR_IBEAM)

        if event == QUIT:
            app_running = False
        if event == MW_UP or (event == CTRL_UP and can_update): # Le scroll par de 0 en haut vers le bas
            dscroll = input_manager.mw_value
            renderer.scrolly = max(0, renderer.scrolly-dscroll) # la page se dirige vers le bas
            scrollbar_update = True
        if event == MW_DOWN or (event == CTRL_DOWN and can_update):
            dscroll = input_manager.mw_value
            nb_not_visible_lines = max(0, line_manager.nb_lines - settings.MAX_LINES)
            renderer.scrolly = min(nb_not_visible_lines, renderer.scrolly + dscroll)
            scrollbar_update = True
        if event == LEFTCLICK:
            if widget_manager.focused_widget:
                # Increase scroll 
                renderer.scroll = widget_manager.focused_widget.get_scroll(renderer.scroll, line_manager.nb_lines, line_manager.len_longuest_line)
            else:
                mouse_gridpos = input_manager.get_mouse_grid_pos((renderer.font_width, renderer.line_height))
                cursor.set_pos(mouse_gridpos, scroll=renderer.scroll)
                if input_manager.last_event != event:
                    cursor.set_anchor()
        if event == RIGHTCLICK:
            rightclickaction.mainloop()
            outside_event = rightclickaction.action
        if event == CTRL_C and will_update:
            cursor.copy_selection()
        if event == CTRL_X:
            pass
        if event == CTRL_V and will_update:
            clipboard_content = paste()
            addx, addy = line_manager.add_to_line(clipboard_content, cursor.gridpos, get_cursor_repos_info=True)
            cursor.set_pos((cursor.gridposx + addx, cursor.gridposy + addy), renderer.scroll) # Pas idéal, si ?
            cursor.set_anchor()
        if event == CTRL_S and will_update:
            local.save_txtfile("txtfile.txt", line_manager.lines)
        if event == CTRL_L and will_update:
            line_manager.lines = local.load_txtfile("txtfile.txt")
        if event == CTRL_A and will_update:
            cursor.select_all()
        if event == CTRL_M and can_update:
            if console.macro_loaded:
                macro_mode = True
            else:
                print("No macro file loaded")
        if event == CTRL_RIGHT and can_update:
            cursor.set_fullpos_to_word_end()
        if event == CTRL_LEFT and can_update:
            cursor.set_fullpos_to_word_start()
        if event == CTRL_RETURN and can_update:
            cursor.line_return_no_carry()
        if event == UP and will_update:
            cursor.move_up()
            renderer.scroll = cursor.get_updated_scroll(renderer.scroll)
            scrollbar_update = True
        if event == DOWN and will_update:
            cursor.move_down()
            renderer.scroll = cursor.get_updated_scroll(renderer.scroll)
            scrollbar_update = True
        if event == LEFT and will_update:
            cursor.move_left()
        if event == RIGHT and will_update:
            cursor.move_right()
        if event == BACKSPACE and will_update:
            text_selection_indices = cursor.select_indices
            line_manager.remove_selection(text_selection_indices)
            if text_selection_indices[0] == text_selection_indices[1]: # Supprime un caractère
                cursor.move_left()
            else: # Supprime une zone de texte
                cursor.set_pos(text_selection_indices[0], renderer.scroll)
            cursor.anchor = cursor.gridpos
            renderer.scroll = cursor.get_updated_scroll(renderer.scroll)
            scrollbar_update = True
        if event == RETURN and will_update:
            line_manager.add_line_at_cursor(cursor.gridpos)
            cursor.gridposx = 0
            cursor.gridposy += 1
            cursor.set_anchor()
            renderer.scroll = cursor.get_updated_scroll(renderer.scroll)
            scrollbar_update = True
        if input_manager.unicode_event and input_manager.is_only_unicode:
            line_manager.add_char_at_cursor(cursor.gridpos, event)
            cursor.move_right()
        # Event Auxliaires
        if event == UPPER:
            line_manager.upper_line(cursor.gridposy)
        if event == LOWER:
            line_manager.lower_line(cursor.gridposy)
        if event == INSERT_HOUR:
            line_manager.insert_hour(cursor.gridpos)
        if event == INSERT_DATE:
            line_manager.insert_date(cursor.gridpos)
        if event == BG:
            line_manager.change_line_bg(cursor.gridposy)
        if event == FG:
            line_manager.change_line_fg(cursor.gridposy)
        if event == ESCAPE or event == CONSOLE:
            console.mainloop()
            app_running = console.notepad_running

        # Cas particuliers
        if event != LEFTCLICK and input_manager.last_event == LEFTCLICK:
            widget_manager.reset_clicked()
        
        if macro_mode:
            if console.macro_command_idx < len(console.macro_commands):
                console.execute_current_macro_command()
            else:
                macro_mode = False
                console.reset_macro_mode()
        
        if scrollbar_update:
            widget_manager.update_y_bar(renderer.scrolly, line_manager.nb_lines)

        input_manager.set_last_event(event)
        state_master.set_last_event(event)

        cursor.visible = (True if event else False) or state_master.check_cursor_visible()
        renderer.render_lines(lines=line_manager.lines, colored_lines=line_manager.colored_lines)
        xy_start, xy_end = cursor.select_indices
        renderer.render_selection(xy_start, xy_end)
        renderer.render_cursor(cursor.gridpos, cursor.visible)
        renderer.render_scrollbars(widget_manager.widgets)
        renderer.render_cursor_info(cursor.gridpos)
        renderer.update()
        state_master.update_fps_counter()

if __name__ == "__main__":
    main()