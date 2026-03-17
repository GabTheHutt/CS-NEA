import pygame
from Boxes import *

def Show_settings(screen, font, settings_manager):
    small_font = pygame.font.SysFont(None,32)
    in_settings = True
    clock = pygame.time.Clock()
    selected_action = None
    duplicate_timer = None  # Timer to track how long the duplicate warning has been shown

    heading = Heading(0, 80, "SETTINGS", pygame.font.SysFont(None, 70))
    heading.set_position((screen.get_width() - heading.font.size(heading.text)[0]) // 2, 80) #Centers the heading at the top of the screen

    # Volume slider
    volume_slider = Slider(320, 200, 300, 8, 0, 100, settings_manager.get_volume())
    volume_slider.base_y = 200

    #Difficulty slider
    difficulty_slider = Slider(320, 260, 300, 8, 1, 10, settings_manager.get_difficulty())
    difficulty_slider.base_y = 260

    # Enemy Health Toggle
    enemy_health_toggle = Toggle(
    x=500,y=320,  # sits below difficulty slider 
    w=100, h=36,
    initial_value=settings_manager.get_show_enemy_health(),
    settings_manager=settings_manager,
    setting_getter=settings_manager.get_show_enemy_health,
    setting_setter=settings_manager.set_show_enemy_health)
    enemy_health_toggle.base_y = 320

    # Music Toggle instantiation
    # Sits below the enemy health toggle, with the same horizontal position and size
    music_toggle = Toggle(
    x=500,y=380,  # sits below enemy health toggle
    w=100, h=36,
    initial_value=settings_manager.get_music(),
    settings_manager=settings_manager,
    setting_getter=settings_manager.get_music,
    setting_setter=settings_manager.set_music)
    music_toggle.base_y = 380

    # SFX Toggle instantiation
    # Sits below the music toggle, with the same horizontal position and size
    sfx_toggle = Toggle(
    x=500,y=440,  # sits below music toggle
    w=100, h=36,
    initial_value=settings_manager.get_sfx(),
    settings_manager=settings_manager,
    setting_getter=settings_manager.get_sfx,
    setting_setter=settings_manager.set_sfx)
    sfx_toggle.base_y = 440

    # Scroll area for keybinds
    actions = ["shoot", "dash", "left", "right", "jump", "melee", "interact"]
    keybind_font = pygame.font.SysFont(None, 32)

    scroll_area = ScrollArea((screen.get_width() - 500) // 2, 150, 500, 300, content_height=410 + len(actions) * 70)
    LEFT_MARGIN = 40 #Margin for text inside the scroll area

    #Scroll Surface
    scroll_surface = pygame.Surface((scroll_area.rect.w, scroll_area.rect.height)) #Creates a separate surface for the scroll area content, which allows for smoother scrolling and prevents artifacts when scrolling
    scroll_surface.set_colorkey((0,0,0))

    keybind_boxes = []
    y = 520
    for action in actions:
        keybind_boxes.append(KeyBindBox(320, y, 150, 40, action, settings_manager, keybind_font)) 
        y += 70 #Creates a keybind box for each action, which allows the player to change the keybinds

    back_button = Button(x=50,y=screen.get_height() - 120,w=250,h=60,visible=True,text="BACK TO MENU",font=small_font)
    reset_button = Button(x=screen.get_width() - 50 - 250,y=screen.get_height() - 120,w=250,h=60,visible=True,text="RESET TO DEFAULT",font=small_font)

    while in_settings:
        screen.fill((0,0,0))
        heading.draw(screen)

        # Updates the position of the sliders based on the scroll offset, so they will scroll with the keybind boxes
        # Required to update here so that when you scroll back up the sliders and toggles will draw.
        volume_slider.update_position(scroll_area.offset) 
        difficulty_slider.update_position(scroll_area.offset)
        enemy_health_toggle.update_position(scroll_area.offset)
        music_toggle.update_position(scroll_area.offset)
        sfx_toggle.update_position(scroll_area.offset)

        # Scroll area background
        scroll_surface.fill((40,40,40))

        pygame.draw.rect(screen, (40,40,40), scroll_area.rect)

        visible_top = scroll_area.rect.top
        visible_bottom = scroll_area.rect.bottom
        #Calculates the visible area of the scroll content
        
        # Draw volume slider
        if volume_slider.rect.bottom >= visible_top and volume_slider.rect.top <= visible_bottom:
            vol_label = font.render("Volume:", True, (255,255,255))
            scroll_surface.blit(vol_label, (LEFT_MARGIN, volume_slider.rect.y - scroll_area.rect.y - 10))
            volume_slider.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # Draw difficulty slider
        if difficulty_slider.rect.bottom >= visible_top and difficulty_slider.rect.top <= visible_bottom:
            diff_label = font.render("Difficulty:", True, (255,255,255))
            scroll_surface.blit(diff_label,(LEFT_MARGIN, difficulty_slider.rect.y - scroll_area.rect.y - 10))
            difficulty_slider.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # Draw enemy health toggle
        if enemy_health_toggle.rect.bottom >= visible_top and enemy_health_toggle.rect.top <= visible_bottom:
            toggle_label = font.render("Enemy Health Bar:", True, (255, 255, 255))
            scroll_surface.blit(toggle_label, (LEFT_MARGIN, 
                                enemy_health_toggle.rect.y - scroll_area.rect.y + 8))
            enemy_health_toggle.update_position(scroll_area.offset)
            enemy_health_toggle.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # Draw music toggle
        if music_toggle.rect.bottom >= visible_top and music_toggle.rect.top <= visible_bottom:
            music_label = font.render("Music:", True, (255, 255, 255))
            scroll_surface.blit(music_label, (LEFT_MARGIN, 
                                music_toggle.rect.y - scroll_area.rect.y + 8))
            music_toggle.update_position(scroll_area.offset)
            music_toggle.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # Draw sfx toggle
        if sfx_toggle.rect.bottom >= visible_top and sfx_toggle.rect.top <= visible_bottom:
            sfx_label = font.render("Sound Effects:", True, (255, 255, 255))
            scroll_surface.blit(sfx_label, (LEFT_MARGIN, 
                                sfx_toggle.rect.y - scroll_area.rect.y + 8))
            sfx_toggle.update_position(scroll_area.offset)
            sfx_toggle.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)

        # Draw keybinds inside scroll area
        for kb in keybind_boxes:
            kb.update_position(scroll_area.offset)
            if kb.active:
                selected_action = kb.action

            if kb.rect.bottom >= visible_top and kb.rect.top <= visible_bottom:
                label = keybind_font.render(kb.action.capitalize(), True, (255,255,255))
                scroll_surface.blit(label, (LEFT_MARGIN, kb.rect.y - scroll_area.rect.y + 10))
                kb.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # De-selects current action, deleting the prompt
        if not any(kb.active for kb in keybind_boxes):
            selected_action = None

        screen.blit(scroll_surface, scroll_area.rect.topleft) 
        #Draws the scroll surface onto the main screen at the position of the scroll area

        #Shows a prompt for that keybind box when active
        if selected_action:
            prompt_font = pygame.font.SysFont(None, 32)
            line1 = prompt_font.render("Press a key for:", True, (255, 215, 0))
            line2 = prompt_font.render(selected_action.capitalize(), True, (255, 215, 0)) #Displays the name of the action being re-bound in uppercase for clarity
            x = screen.get_width() - line1.get_width() - 20
            y = screen.get_height() // 2
            screen.blit(line1, (x, y))
            centered_x = x + (line1.get_width() - line2.get_width()) // 2 #Calculates the x position
            screen.blit(line2, (centered_x, y + 35)) #Centres the second prompt line

        #Displays a warning message for 3 seconds.
        if duplicate_timer and pygame.time.get_ticks() - duplicate_timer < 3000: 
            warn = prompt_font.render("Key already in use!", True, (255, 50, 50))
            warn_x = screen.get_width() - warn.get_width() - 20
            warn_y = screen.get_height() // 2 + 80
            screen.blit(warn, (warn_x, warn_y))

        back_button.draw(screen)
        reset_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle events for sliders, scroll area, toggles and keybind boxes
            volume_slider.handle_event(event)
            difficulty_slider.handle_event(event)
            scroll_area.handle_event(event)
            enemy_health_toggle.handle_event(event, scroll_area.rect.x, scroll_area.rect.y)
            music_toggle.handle_event(event, scroll_area.rect.x, scroll_area.rect.y)
            sfx_toggle.handle_event(event, scroll_area.rect.x, scroll_area.rect.y)

            if reset_button.action(event):
                settings_manager.reset_keybinds() #Resets settings to default values
                # Reset sliders to default values
                volume_slider.reset(settings_manager.get_volume())
                difficulty_slider.reset(settings_manager.get_difficulty())
                selected_action = None    #De-selects any active keybind boxes

                # Update all keybind boxes to reflect new defaults
                for kb in keybind_boxes:
                    kb.active = False  # ensure none stay selected

            for kb in keybind_boxes:
                kb.handle_event(event, scroll_area.rect.x, scroll_area.rect.y)
                if kb.active:
                    selected_action = kb.action #Sets the selected action to the active keybind box
                if kb.duplicate:
                    duplicate_timer = pygame.time.get_ticks()  # Start the timer when a duplicate keybind is detected
                    kb.duplicate = False  # Reset the duplicate flag to prevent multiple timers

            # Save the settings and return to the main menu
            if back_button.action(event):
                settings_manager.set_volume(volume_slider.value)
                settings_manager.set_difficulty(difficulty_slider.value)
                settings_manager.save()
                in_settings = False

        pygame.display.update()
        clock.tick(60)