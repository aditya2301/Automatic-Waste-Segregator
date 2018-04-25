import lcd
import time

 while True:
    # Send some text
    lcd.lcd_string("Automatic Waste ",LCD_LINE_1)
    lcd.lcd_string("   Segregation  ",LCD_LINE_2)
 
    time.sleep(3)
      
    # Send some test
    lcd.lcd_string("Object Detected!",LCD_LINE_1)
    time.sleep(1)
    lcd.lcd_string("                ",LCD_LINE_1)
    lcd.lcd_string("Sorting         ",LCD_LINE_2)
    
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd.lcd_string("Object is ",LCD_LINE_1)
    if binDir=='l':
        lcd.lcd_string(" Biodegradable ",LCD_LINE_2)
    else:
        lcd.lcd_string("     Non-Bio    ",LCD_LINE_2)

    time.sleep(3) # 3 second delay
 
   