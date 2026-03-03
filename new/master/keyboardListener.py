from pynput import keyboard

numbers_list = list("1234567890")

valid_year_list = {
    "1930": "1930", "1934": "1934", "1938": "1938",
    "1942": "1942", "1946": "1946", "1950": "1950",
    "1954": "1954", "1958": "1958", "1962": "1962",
    "1966": "1966", "1970": "1970", "1974": "1974",
    "1978": "1978", "1982": "1982", "1986": "1986",
    "1990": "1990", "1994": "1994", "1998": "1998",
    "2002": "2002", "2006": "2006", "2010": "2010",
    "2014": "2014", "2018": "2018", "2022": "2022",
    "2026": "2026", "2030": "2030", "2034": "2034",
    "2038": "2038", "2042": "2042", "2046": "2046",
    "2050": "2050", "2054": "2054", "2058": "2058",
    "2062": "2062", "2066": "2066", "2070": "2070",
    "2074": "2074", "2078": "2078", "2082": "2082",
    "2086": "2086", "2090": "2090", "2094": "2094",
    "2098": "2098", "2102": "2102", "2106": "2106",
    "2110": "2110", "2114": "2114", "2118": "2118",
    "2122": "2122", "2126": "2126", "2130": "2130",
    "2134": "2134"
}


class KeyboardListener:
    def __init__(
        self,
        on_valid_year,
        on_update_display,
        on_stop_video,
        on_volume_up=None,
        on_volume_down=None,
        on_volume_mute=None,
    ):
        self.year = ""
        self.on_valid_year = on_valid_year
        self.on_update_display = on_update_display
        self.on_stop_video = on_stop_video
        self.on_volume_up = on_volume_up
        self.on_volume_down = on_volume_down
        self.on_volume_mute = on_volume_mute

    def on_press(self, key):
        try:
            char = key.char
            if char in numbers_list:
                self._add_number(char)

        except AttributeError:
            # --- Special keys ---
            if key == keyboard.Key.backspace:
                if self.year == "":
                    self.on_stop_video()
                else:
                    self.year = self.year[:-1]
                    self.on_update_display(self.year)

            elif key == keyboard.Key.enter:
                self._check_year()

            # --- Media keys ---
            elif key == keyboard.Key.media_volume_up:
                if self.on_volume_up:
                    self.on_volume_up()

            elif key == keyboard.Key.media_volume_down:
                if self.on_volume_down:
                    self.on_volume_down()

            elif key == keyboard.Key.media_volume_mute:
                if self.on_volume_mute:
                    self.on_volume_mute()

    def _add_number(self, char):
        if len(self.year) < 4:
            self.year += char
            self.on_update_display(self.year)

    def _check_year(self):
        if len(self.year) == 4 and self.year in valid_year_list:
            video = valid_year_list[self.year]
            self.on_valid_year(self.year, video)

        # Always reset after Enter
        self.year = ""
        self.on_update_display(self.year)

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()