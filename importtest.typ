#show :main=>{
  let rotateChar =  "[ー\u{FF5E}\u{301C}\p{Open_Punctuation}\p{Close_Punctuation}a-zA-Z0-9]"
  set align(right)
  let b
//  main.children.at(2).fields()

//文章全体を分割して積み上げ
stack(
  dir:rtl,
  spacing: 1em,
  ..if main.has("children"){
  for s in main.children{
    //bodyに本文が含まれている構文の場合
    if s.has("body"){
      if s.at("body").has("children"){
        for t in s.at("body").children{
          if t.has("text"){
            stack(dir:ttb,1em,
              ..for u in t.at("text"){
                u
              }
              ,)
          }
        }
      }
    }
  }
  }
  ,)
  b
}
  *aaaaaaaaaaaaaaaaaaaaaaaaaaaa  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*