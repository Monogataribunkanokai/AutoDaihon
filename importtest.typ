#show :main=>{
  let rotateChar =  "[ー\u{FF5E}\u{301C}\p{Open_Punctuation}\p{Close_Punctuation}a-zA-Z0-9]"
  //set align(right)
  let b
//  main.children.at(0).func()

//文章全体を分割して積み上げ
stack(
  dir:rtl,
  spacing: 1em,
  ..if(main.has("children")){
    //b="children判定突破"
  for s in main.children{
    //bodyに本文が含まれている構文の場合
    if s.func()==text{
      b="テキスト判定突破 \n"
          b=s
            stack(dir:ttb,0.3em,
              ..for t in s.at("text"){
                  rotate(90deg,t)
                },
              )
        }
    else {
      }
  }
  }
  else{
    b="childrenなし"
    }
  ,)
  b
}
aaaaa bbbbb ccccc