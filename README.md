# 项目介绍
- 原github作者[ tianshipapa ](https://github.com/tianshipapa) 和 [ymyuuu](https://github.com/ymyuuu/BestDomain)
- 老王只是合并两个项目
- github项目地址 https://github.com/jc-lw/youxuanyuming

![image.png](https://rin.vcrr.us.kg/images/18b0be4bca205491b1aaf70983319fe504bef426.png)




## cloudflare IP 抓取原理 

- `collect_ips.py`文件 是抓取优选IP的网站, `bestdomain.py`是把抓取的IP写入到cloudflare的DNS解析中
- 抓取 https://ip.164746.xyz 和 https://cf.090227.xyz 的优选ip，写入ip.txt 
- 相关项目 [cf-speed-dns](https://github.com/zhixuanwang/cf-speed-dns)

![image.png](https://rin.vcrr.us.kg/images/51e6dd9bbb99f98d3241509b804d98a4fc1fa5db.png)



## Usage 项目使用方法 

### collect_ips.py 抓取优选IP

- Fork 本项目, 修改以下文件, 然后通过 Github Actions 定时运行

- 修改 `caijiip.yml` 文件中 git的提交信息 改成你自己的，否则报错
![image.png](https://rin.vcrr.us.kg/images/0ddaaecae1242f12aadaa847662d56a23398cda5.png)

- `collect_ips.py`文件 这里是抓取优选IP的网站列表，如需要可自行修改, 同时抓取规则也要相应修改
![image.png](https://rin.vcrr.us.kg/images/38a3d57288da468b17964664e54da54a4175ba0e.png)


### bestdomain.py 用于修改cloudflare的DNS记录 

- 修改 `bestdomain.py` 文件中的ip列表源地址, 改为你的仓库域名开头, 通过下面的方法获取你的仓库链接地址
![image.png](https://rin.vcrr.us.kg/images/85362a2f5680355d4d73a2293ce82099c42e3308.png)
![image.png](https://rin.vcrr.us.kg/images/5def5f757d7a63978358e5a950714bed3dc6c213.png)

- 在 `bestdomain.py` 文件中修改成 上面复制链接, 因为你抓取优选ip可能跟我不一样。注意每个子域名可以对应不同的IP源地址
![image.png](https://rin.vcrr.us.kg/images/52f07d0b88279fb13694e1071d3184082408cf3d.png)


### 获取 Cloudflare API令牌

1. 创建 Cloudflare API 令牌
访问 [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)

2. 选择需要解析的域名，创建编辑 DNS 权限的` CF_API_TOKEN`
![image.png](https://rin.vcrr.us.kg/images/35feefcde1ed0cc08e430e419de73b892157d35c.png)


3. 在你的 GitHub 仓库中，设置 `CF_API_TOKEN `为你的 Cloudflare API 令牌
![image.png](https://rin.vcrr.us.kg/images/004eb6d2c8441cfa266129b3906e43e60bf99090.png)


4. 配置 GitHub Actions 定时任务
- 编辑 [.github/workflows/main.yml](.github/workflows/main.yml) 文件，设置 `cron` 表达式以定义任务运行时间间隔


### 设置完成 需要手动开启Actions
- ![image.png](https://rin.vcrr.us.kg/images/defa31617244ae82e89f05480be397eb3938f15e.png)

### 测试域名是否成功
- 去 https://www.itdog.cn/http/ 测试你的域名, 查看ping出来的优选IP是否正确
![image.png](https://rin.vcrr.us.kg/images/8816d5204054629815ecf6add95e9e244849e85b.png)

