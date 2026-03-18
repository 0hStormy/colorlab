import colorlab as cl

ok = cl.Oklab.from_srgb(cl.Rgb(40, 85, 12))
print(f"oklab: {ok.lightness} {ok.a} {ok.b}")