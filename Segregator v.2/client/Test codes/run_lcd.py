import lcd
import time

binDir='r'
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

lcd.main()

 
    # Send some test
lcd.lcd_string("Automatic Waste",LCD_LINE_1)
lcd.lcd_string("Segregation",LCD_LINE_2)
 
time.sleep(3) # 3 second delay
 
    # Send some text
lcd.lcd_string("Alert!!!",LCD_LINE_1)
lcd.lcd_string("Object Detected",LCD_LINE_2)
 
time.sleep(3) # 3 second delay
 
    # Send some text
lcd.lcd_string("Waste Detected:",LCD_LINE_1)
if binDir=='l':
    lcd.lcd_string("Biodegradable",LCD_LINE_2)
elif binDir=='r':
    lcd.lcd_string("Non-Bio",LCD_LINE_2)
 
time.sleep(3)
 
    # Send some text
lcd.lcd_string("Alert!!!",LCD_LINE_1)
if binDir=='l':
    lcd.lcd_string("Bio bin full",LCD_LINE_2)
elif binDir=='r':
    lcd.lcd_string("Non-Bio bin full",LCD_LINE_2)
 
time.sleep(3)
   