
class ColorHSV:
    def __init__(self, hue=0, saturation=0, value=0):
        self.hue = hue if hue < 359 else 359
        self.saturation = saturation
        self.value = value

    def lerp(self, color, amount):
        return ColorHSV(
            self.hue + (color.hue - self.hue) * amount,
            self.saturation + (color.saturation - self.saturation) * amount,
            self.value + (color.value - self.value) * amount
        )

    @classmethod
    def from_rgb(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df / mx) * 100
        v = mx * 100
        return self(h, s, v)

    def get_rgb(self):

        h, s, v = self.hue, self.saturation, self.value
        c = v * s
        h /= 60
        x = c * (1 - abs((h % 2) - 1))
        m = v - c

        if h < 1:
            res = (c, x, 0)
        elif h < 2:
            res = (x, c, 0)
        elif h < 3:
            res = (0, c, x)
        elif h < 4:
            res = (0, x, c)
        elif h < 5:
            res = (x, 0, c)
        elif h < 6:
            res = (c, 0, x)
        else:
            raise Exception("Unable to convert from HSV to RGB")

        r, g, b = res
        return round((r + m) * 255, 3), round((g + m) * 255, 3), round((b + m) * 255, 3)