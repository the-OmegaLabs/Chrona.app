import sys
import Frameworks.Logger as Logger
import Frameworks.Utils as Utils
from PIL import Image  

import maliang
import maliang.animation

class Application:
    def getScaled(self, number: float) -> int:
        return int(number * self.UI_SCALE)

    def __init__(self, args):
        Logger.output('Starting Chrona...')

        self.bus          = args 
        self.IS_DEVMODE   = args.IS_DEVMODE   

        self.UI_SCALE     = args.UI_SCALE     
        self.UI_FPS       = args.UI_FPS       
        self.UI_THEME     = args.UI_THEME 
        self.UI_ANIMATIME = args.UI_ANIMATIME
        self.UI_LOCALE    = args.UI_LOCALE
        self.UI_FAMILY    = args.UI_FAMILY

        self.UI_WIDTH     = self.getScaled(1000)
        self.UI_HEIGHT    = self.getScaled(795)

        self.SET_MUTE     = args.SET_MUTE
        
        self.WDGS_tooltip = []

        self.loadImage()
        self.createWindow()
        self.loadWidget()


        self.root.mainloop()

    def loadImage(self):
        try:
            self.IMG_icon = Image.open('./Resources/icon.png')
            
            self.IMG_sona = Image.open('./Resources/sona.png')
            self.IMG_alarm = Image.open('./Resources/alarm.png')
            self.IMG_timer = Image.open('./Resources/timer.png')
            self.IMG_stopwatch = Image.open('./Resources/stopwatch.png')  
            self.IMG_setting = Image.open('./Resources/settings.png')
            self.IMG_theme = Image.open('./Resources/theme.png')
            self.IMG_notify = Image.open('./Resources/notify.png')

            self.APP_menuicon = [self.IMG_sona, self.IMG_timer, self.IMG_alarm, self.IMG_stopwatch]
        except Exception as e:
            Logger.output(f"Error loading images: {e}", type=Logger.Type.ERROR)
            sys.exit()

    def createWindow(self):
        self.root = maliang.Tk(size=(self.UI_WIDTH, self.UI_HEIGHT))

        self.root.title('Chrona')
        self.root.icon(maliang.PhotoImage(self.IMG_icon.resize(size=(32, 32), resample=1)))

        self.root.maxsize(self.UI_WIDTH, self.UI_HEIGHT)
        self.root.minsize(self.UI_WIDTH, self.UI_HEIGHT)

        self.cv = maliang.Canvas(self.root)
        self.cv.place(x=0, y=0, width=self.UI_WIDTH, height=self.UI_HEIGHT)

        # maliang.Env.system = 'Windows10'

    def changePage(self, i):
        if i > 3:
            self.WDG_menubar.set(5)
            self.WDG_setting_button.set(True)
        else:
            self.WDG_menubar.set(i)
            self.WDG_setting_button.set(False)

        if i == 0:
            self.WDG_content_sona.lift()
        if i == 1:
            self.WDG_content_timer.lift()
        if i == 2:
            self.WDG_content_alarm.lift()
        if i == 3:
            self.WDG_content_stopwatch.lift()
        if i == 4:
            self.WDG_content_settings.lift()

        for widget in self.WDGS_tooltip:
            widget.lift()

        maliang.animation.MoveWidget(self.WDG_content_settings, offset=(0, self.getScaled(200)), duration=0, controller=maliang.animation.ease_out, fps=self.UI_FPS).start()
        maliang.animation.MoveWidget(self.WDG_content_settings, offset=(0, self.getScaled(-200)), duration=int(self.UI_ANIMATIME ), controller=maliang.animation.ease_out, fps=self.UI_FPS).start()


    def loadWidget(self):
        def generateMenubar():
            self.WDG_menubar = maliang.SegmentedButton(self.cv, position=(self.getScaled(1), self.getScaled(5)), layout='vertical', family=self.UI_FAMILY, fontsize=self.getScaled(15), text=self.APP_menulist, command=self.changePage, default=0)
            self.WDG_menubar.style.set(bg=('', ''), ol=('', ''))

            for i, item in enumerate(self.WDG_menubar.children): 
                maliang.Image(item, position=(item.size[1] // 2, item.size[1] // 2 + self.getScaled(1)), anchor='center', image=(maliang.PhotoImage(self.APP_menuicon[i].resize((self.getScaled(30), self.getScaled(30)), 1))))
                item.style.set(ol=('', '', '', '', '', ''), bg=('', '#292929', '#292929', '#2D2D2D', '#292929', '#2D2D2D'))

            self.WDG_setting_button = maliang.ToggleButton(self.cv, position=(self.APP_sidebar_width // 2, self.UI_HEIGHT - self.WDG_menubar.children[0].size[0] // 2 - self.getScaled(7)), anchor='center', size=self.WDG_menubar.children[0].size, command=lambda _: self.changePage(4))
            self.WDG_setting_button.style.set(ol=('', '', '', '', '', ''), bg=('', '#292929', '#292929', '#2D2D2D', '#292929', '#2D2D2D'))

            maliang.Image(self.WDG_setting_button, position=(0, self.getScaled(1)), anchor='center', image=(maliang.PhotoImage(self.IMG_setting.resize((self.getScaled(30), self.getScaled(30)), 1))))    

            for i, item in enumerate(self.WDG_menubar.children): 
                self.WDGS_tooltip.append(maliang.Tooltip(item, text=self.APP_menulist_text[i], align='right', family=self.UI_FAMILY, fontsize=self.getScaled(15)))

            self.WDGS_tooltip.append(maliang.Tooltip(self.WDG_setting_button, text='Settings', align='right', family=self.UI_FAMILY, fontsize=self.getScaled(15)))

        def generateSettingsPage():
            content_start_at = self.getScaled(55)
            title = maliang.Text(self.WDG_content_settings, position=(content_start_at, self.getScaled(30)), text='Settings', family=self.UI_FAMILY, fontsize=self.getScaled(40), weight='bold')

            general = maliang.Text(self.WDG_content_settings, position=(content_start_at, self.getScaled(140)), text='General', family=self.UI_FAMILY, fontsize=self.getScaled(17), weight='bold')

            theme_label = maliang.Label(self.WDG_content_settings, position=(content_start_at, self.getScaled(175)), size=(self.WDG_content_settings.size[0] - content_start_at * 2, self.getScaled(70)), family=self.UI_FAMILY, fontsize=self.getScaled(17), weight='bold')
            theme_label.style.set(ol=('#233232', '#233232'), bg=('#323232', '#393939'))            
            theme_icon = maliang.Image(theme_label, position=(self.getScaled(70) // 2, self.getScaled(70) // 2 + self.getScaled(2)), anchor='center', image=(maliang.PhotoImage(self.IMG_theme.resize((self.getScaled(45), self.getScaled(45)), 1))))
            theme_title = maliang.Text(theme_label, position=(self.getScaled(65), self.getScaled(15)), text='App theme', family=self.UI_FAMILY, fontsize=self.getScaled(15))
            theme_description = maliang.Text(theme_label, position=(self.getScaled(65), self.getScaled(36)), text='Choose the theme of the app.', family=self.UI_FAMILY, fontsize=self.getScaled(14))
            theme_description.style.set(fg=('#A0A0A0'))
            theme_menu = maliang.SegmentedButton(theme_label, layout='horizontal', position=(theme_label.size[0] - self.getScaled(20), theme_label.size[1] // 2), anchor='e', family=self.UI_FAMILY, fontsize=self.getScaled(15), text=['Light', 'Dark', 'System'], default=2)
            theme_menu.style.set(bg=['#343434', '#343434'])
            for item in theme_menu.children: 
                item.style.set(ol=('', '', '', '', '', ''), bg=('', '#292929', '#292929', '#2D2D2D', '#292929', '#2D2D2D'))

            notify_label = maliang.Label(self.WDG_content_settings, position=(content_start_at, self.getScaled(250)), size=(self.WDG_content_settings.size[0] - content_start_at * 2, self.getScaled(70)), family=self.UI_FAMILY, fontsize=self.getScaled(17), weight='bold')
            notify_label.style.set(ol=('#233232', '#233232'), bg=('#323232', '#393939'))            
            notify_icon = maliang.Image(notify_label, position=(self.getScaled(70) // 2, self.getScaled(70) // 2 + self.getScaled(0)), anchor='center', image=(maliang.PhotoImage(self.IMG_notify.resize((self.getScaled(45), self.getScaled(45)), 1))))
            notify_title = maliang.Text(notify_label, position=(self.getScaled(65), self.getScaled(15)), text='Notifications', family=self.UI_FAMILY, fontsize=self.getScaled(15))
            notify_description = maliang.Text(notify_label, position=(self.getScaled(65), self.getScaled(36)), text='Modify your notification settings.', family=self.UI_FAMILY, fontsize=self.getScaled(14))
            notify_description.style.set(fg=('#A0A0A0'))
            
            notify_managedBySysText = maliang.Text(notify_label, anchor='e', position=(notify_label.size[0] - self.getScaled(20), notify_label.size[1] // 2), text='Managed by Desktop Bus', family=self.UI_FAMILY, fontsize=self.getScaled(15))
            notify_managedBySysText.style.set(fg=('#A0A0A0'))

        self.APP_sidebar_width = self.getScaled(45)

        self.APP_menulist = [
            ' ' * 5,
            ' ' * 5,
            ' ' * 5,
            ' ' * 5,
        ]

        self.APP_menulist_text = [
            'Sona',
            'Timer',
            'Alarm',
            'Stopwatch'
        ]

        generateMenubar()
                
        self.bg = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(0)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))
        self.bg.style.set(ol=('', ''), bg=('#272727', '#272727'))
        
        self.WDG_content_sona      = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(-5)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))
        self.WDG_content_timer     = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(-5)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))
        self.WDG_content_alarm     = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(-5)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))
        self.WDG_content_stopwatch = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(-5)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))
        self.WDG_content_settings  = maliang.Label(self.cv, position=(self.APP_sidebar_width, self.getScaled(-5)), size=(self.UI_WIDTH - self.APP_sidebar_width, self.UI_HEIGHT + self.getScaled(10)))

        self.WDG_content_sona      .style.set(ol=('', ''), bg=('#272727', '#272727'))
        self.WDG_content_timer     .style.set(ol=('', ''), bg=('#272727', '#272727'))
        self.WDG_content_alarm     .style.set(ol=('', ''), bg=('#272727', '#272727'))
        self.WDG_content_stopwatch .style.set(ol=('', ''), bg=('#272727', '#272727'))
        self.WDG_content_settings  .style.set(ol=('', ''), bg=('#272727', '#272727'))
            
        generateSettingsPage()

        self.changePage(4)