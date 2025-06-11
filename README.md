# 项目介绍
- 原github作者[ tianshipapa ](https://github.com/tianshipapa) 和 [ymyuuu](https://github.com/ymyuuu/BestDomain)
- 老王只是合并两个项目
- github项目地址 https://github.com/jc-lw/youxuanyuming



## cloudflare IP 抓取原理 

- `collect_ips.py`文件 是抓取优选IP的网站. `bestdomain.py`是把抓取的IP写入到cloudflare的DNS解析中

- 抓取以下网站优选ip, 写入 ip.txt. 网站列表如下
1. https://stock.hostmonit.com/CloudFlareYes 
2. https://cf.090227.xyz 
3. https://ip.164746.xyz 
4. https://ipdb.api.030101.xyz/?type=bestcf&country=true

- 相关项目 [cf-speed-dns](https://github.com/zhixuanwang/cf-speed-dns)



## Usage 项目使用方法 

### collect_ips.py 抓取优选IP

- Fork 本项目, 修改以下文件, 然后通过 Github Actions 定时运行

- 修改 `caijiip.yml` 文件中 git的提交信息 改成你自己的，否则报错
![image.png](https://camo.githubusercontent.com/c6a5c24050a2d5cfef7d9f824aff2ba572171871ceb11efcc48bb3087ad7bdd0/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f306464616165636165313234326631326161646161383437363632643536613233333938636461352e706e67)

- `collect_ips.py`文件 这里是抓取优选IP的网站列表，如需要可自行修改, 同时抓取规则也要相应修改
![image.png](https://camo.githubusercontent.com/705905d2cb44d5b7619609d3e7a03cded38e0e0868a506079fc77d0417d085bf/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f333861336435373238386461343638623137393634363634653534646135346134313735626130652e706e67)


### bestdomain.py 用于修改cloudflare的DNS记录 

- 修改 `bestdomain.py` 文件中的ip列表源地址, 改为你的仓库域名开头, 通过下面的方法获取你的仓库链接地址
![image.png](https://camo.githubusercontent.com/9db5361d2bac6ab55849417bad118101c91e789a8c424dbf11e2b00765b24e44/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f383533363261326635363830333535643464373361323239336365383230393963343265333330382e706e67)
![image.png](https://camo.githubusercontent.com/0c2539b0140ae72109a1946d7a7a7d95d12a266d80ba78e578e6c9d94ce3c3e7/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f356465663566373537643761363339373833353865356139353037313462656433646336633231332e706e67)

- 在 `bestdomain.py` 文件中修改成 上面复制链接, 因为你抓取优选ip可能跟我不一样。注意每个子域名可以对应不同的IP源地址
![image.png](https://camo.githubusercontent.com/50fbe9a5ada05158426e978e318a89ab51896020504b37938e244af4a5c36b0f/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f353266303764306238383237396662313336393465313037316433313834303832343038636633642e706e67)


### 获取 Cloudflare API令牌

1. 创建 Cloudflare API 令牌
访问 [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)

2. 选择需要解析的域名，创建编辑 DNS 权限的` CF_API_TOKEN`
![image.png](https://camo.githubusercontent.com/bb58131f449fdd6ffd686b5fdbfa7a3d03ff798852b45fe39a5ab4a85fd0edc1/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f333566656566636465316564306363303865343330653431396465373362383932313537643335632e706e67)


3. 在你的 GitHub 仓库中，设置 `CF_API_TOKEN `为你的 Cloudflare API 令牌
![image.png](https://camo.githubusercontent.com/53ccdaaf9e81c3cbaefaad8bdd7ed55e8ebca47048a76f3fb63dc648d767de46/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f303034656236643263383434316366613236363132396233393036653433653630626639393039302e706e67)


4. 配置 GitHub Actions 定时任务
- 编辑 [.github/workflows/main.yml](.github/workflows/main.yml) 文件，设置 `cron` 表达式以定义任务运行时间间隔


### 设置完成 需要手动开启Actions
- ![image.png](https://camo.githubusercontent.com/90aaf91a428804046519c5f13de329e017217be81bd42d590061057892fccf42/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f646566613331363137323434616538326538396630353438306265333937656233393338663135652e706e67)

### 测试域名是否成功
- 去 https://www.itdog.cn/http/ 测试你的域名, 查看ping出来的优选IP是否正确
![image.png](https://camo.githubusercontent.com/2dc428d8792cf7f73e4d932963a595b5680a0e67549a5c1227f1a66cd785b6fd/68747470733a2f2f696d672e6b6a7a6c2e6d652f696d616765732f383831366435323034303534363239383135656366366164643935653965323434383439653835622e706e67)

