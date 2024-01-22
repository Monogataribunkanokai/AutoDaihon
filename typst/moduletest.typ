#let rotateChar = "[ー\u{FF5E}\u{301C}\p{Open_Punctuation}\p{Close_Punctuation}a-zA-Z0-9]"
#let vw( body, size: 13.5pt, font: "Harano Aji Gothic", weight: "regular",
        kerning: 0.3em, leading: 0.5em, spacing: 1em, ) = {
  set text(size: size, font: font, weight: weight)
  set align(right)
  stack( dir: rtl, spacing: leading,
    ..for s in body.split(regex("[\n]")) {
      // "s"
      ( // 1 ->
        stack(dir: ttb, spacing: spacing,
          ..for t in s.split(regex("[\p{Zs}]")) {
            // "t"
            ( // 2 ->
              stack( dir: ttb, spacing: kerning,
                ..for l in t.clusters() {
                  // "l"
                  ( // 3 ->
                    if regex(rotateChar) in l {
                      set align(center)
                      rotate(90deg, l)
                    } else {
                      set align(center)
                      l
                    },
                  ) // <- 3
                }
              ),
            ) // <- 2
          }
        ),
      ) // <- 1
    }
  )
}