# 发布消息 #

> 发布消息是通过 URL GET 的方式来调用的
> ## 地址： ##
> > http://www.tmitter.com/api/note/add/

> ## 参数： ##
    * **uname** 用户名
    * **pwd** 密码<sup>未加密</sup>的
    * **msg** 要发布的消息内容
    * **from** _可以为空_  调用者名称，如：“饭否”，哪么消息里面将显示“通过饭否”，这里最多支持20个字符
> ## 返回值： ##
> > 此API的返回值是通过Response出来的
    * 1 成功
    * -1 出错
    * -2 用户名或密码不正确

> ## 例如： ##
> > http://www.twitter.com/api/note/add/?uname=user1&pwd=123123&msg=这里是要发布的消息&from=Twitter