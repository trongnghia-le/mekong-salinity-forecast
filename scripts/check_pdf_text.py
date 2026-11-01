import sys, fitz
for p in sys.argv[1:]:
    d = fitz.open(p); t = "".join(pg.get_text() for pg in d)
    low = t.lower()
    print(p.split("/")[-1], "pages", len(d), "chars", len(t),
          "| Bang1" , "bảng 1" in low, "| Bang2", "bảng 2" in low,
          "| Cầu Quan", "cầu quan" in low, "| Sơn Đốc", "sơn đốc" in low)
