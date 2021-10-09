# wyycg_checkin
网易云游戏平台签到脚本 Github Action 版

## cookie 获取方法
去网易云游戏页面打开开发者工具，刷新一下，能看到sign-info和sign-user-info的request，在里面找找有的request带有Authorization字段，把那个复制过来就可以了。

![截屏2021-10-09 09 41 27](https://user-images.githubusercontent.com/32559715/136639499-a73ba30b-0aa2-4754-b5ce-f6e8057bf94a.png)

注意获取完了不要注销，如果想退出登录手动删除自己浏览器在这个网站上的cookie就行了。