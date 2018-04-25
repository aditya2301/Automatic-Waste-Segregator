import lcd
import time

 while True:
 
    # Send some test
    lcd.lcd_string("Electronics Hub ",LCD_LINE_1)
    lcd.lcd_string("    Presents    ",LCD_LINE_2)
    
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd.lcd_string("Rasbperry Pi",LCD_LINE_1)
    lcd.lcd_string("16x2 LCD Test",LCD_LINE_2)

    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd.lcd_string("1234567890*@$#%&",LCD_LINE_1)
    lcd.lcd_string("abcdefghijklmnop",LCD_LINE_2)
 
    time.sleep(3)
      