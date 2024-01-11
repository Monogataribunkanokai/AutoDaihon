#show :main=>{
  let rotateChar =  "[ー\u{FF5E}\u{301C}\p{Open_Punctuation}\p{Close_Punctuation}a-zA-Z0-9]"
  set align(right)
  //main.children.at(0).fields()
  for s in main.children{
    if s.has("text"){
      stack(dir: ttb,spacing: 1em,
      ..for t in (s.text.split("[\p{Zs}]")) {
        
    },
      )
    }
  }
}
aaaaaaaa *aa* aaaaaaaaaaabbbba\
aaaaa\
