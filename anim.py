import os, json, time, requests, sys, re, hmac, hashlib, random, pytz, math
from datetime import datetime
import urllib.parse
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.box import HEAVY_EDGE, ROUNDED
from rich.layout import Layout
from rich.live import Live
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.columns import Columns
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import track
from rich.rule import Rule

def calc(i, s, a, o, d, g):
    st = (10 * i + max(0, 1200 - 10 * s) + 2000) * (1 + o / a) / 10
    return math.floor(st) + value(g)

def generate_hash(key, message):
    hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)

def value(input_str):
    return sum(ord(char) for char in input_str) / 1e5

def animate_banner():
    banner = [
        "███    ███ ██████  ██████  ████████ ███████  ██████ ██   ██  ",
        "████  ████ ██   ██ ██   ██    ██    ██      ██      ██   ██  ",
        "██ ████ ██ ██████  ██████     ██    █████   ██      ███████  ",
        "██  ██  ██ ██   ██ ██         ██    ██      ██      ██   ██  ",
        "██      ██ ██   ██ ██         ██    ███████  ██████ ██   ██  "
    ]
    
    colors = ["cyan", "blue", "green", "yellow", "magenta", "red"]
    
    for _ in range(10):  # Animate for 10 cycles
        for i, line in enumerate(banner):
            color = colors[i % len(colors)]
            rprint(f"[{color}]{line}[/{color}]")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        colors = colors[1:] + [colors[0]]  # Rotate colors

def animate_header_footer():
    header = "ByBit Sweeper"
    body = "Welcome to the Hacker's Paradise"
    footer = "Proceed with caution..."
    
    for _ in range(5):  # Animate for 5 cycles
        rprint(Panel(f"[cyan]{header}[/cyan]", border_style="cyan"))
        time.sleep(0.3)
        rprint(Panel(f"[green]{body}[/green]", border_style="green"))
        time.sleep(0.3)
        rprint(Panel(f"[yellow]{footer}[/yellow]", border_style="yellow"))
        time.sleep(0.3)
        os.system('cls' if os.name == 'nt' else 'clear')

def animated_input(prompt):
    for char in prompt:
        rprint(f"[cyan]{char}[/cyan]", end='', flush=True)
        time.sleep(0.05)
    return input()

class ByBit:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,vi-VN;q=0.6,vi;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bybitcoinsweeper.com",
            "Referer": "https://t.me/BybitCoinsweeper_Bot?start=referredBy=695102771",
            "tl-init-data": None,
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36"
        }
        self.info = {"score": 0}

    def log(self, message, level):
        levels = {
            "INFO": "cyan",
            "ERROR": "red",
            "SUCCESS": "green",
            "WARNING": "yellow"
        }
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        console = Console()
        console.print(Panel(f"[white]{current_time}[/white] | [{levels.get(level, 'cyan')}]{level}[/{levels.get(level, 'cyan')}] | {message}", border_style=levels.get(level, 'cyan'), width=60))

    def wait(self, seconds):
        for _ in track(range(seconds), description=f"Waiting for {seconds} seconds..."):
            time.sleep(1)

    def login(self, init_data):
        try:
            self.headers = { "tl-init-data": init_data}
            response = self.session.post("https://api.bybitcoinsweeper.com/api/auth/login", json={"initData": init_data}, headers=self.headers)
            if response.status_code == 201:
                data = response.json()
                self.headers['Authorization'] = f"Bearer {data['accessToken']}"
                return {
                    "success": True,
                    "accessToken": data['accessToken'],
                    "refreshToken": data['refreshToken'],
                    "userId": data['id']
                }
            else:
                return {"success": False, "error": "Unexpected status code"}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}
        
    def userinfo(self):
        try:
            user = self.session.get("https://api.bybitcoinsweeper.com/api/users/me", headers=self.headers).json()
            return user
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}        

    def score_win(self):
            try:
                min_game_time = 70
                max_game_time = 120
                game_time = random.randint(min_game_time, max_game_time)
                playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
                if "message" in playgame:
                    if("expired" in playgame["message"]):
                        self.log("Query Expired Sir", "ERROR")
                        return False
                gameid = playgame["id"]
                rewarddata = playgame["rewards"]
                started_at = playgame["createdAt"]
                userdata = self.userinfo()
                self.log(f"Total Score: {userdata['score']+userdata['scoreFromReferrals']}","SUCCESS")
                unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
                starttime = int(unix_time_started.timestamp() * 1000)
                self.log(f"Starting game {gameid}. Play time: {game_time} seconds", 'INFO')
                self.wait(game_time)
                i = f"{userdata['id']}v$2f1"
                first = f"{i}-{gameid}-{starttime}"
                last = f"{game_time}-{gameid}"
                score = calc(45, game_time, 54, 9, True, gameid)
                game_data = {
                    "bagCoins": rewarddata["bagCoins"],
                    "bits": rewarddata["bits"],
                    "gifts": rewarddata["gifts"],
                    "gameId": gameid,
                    'gameTime': game_time,
                    "h": generate_hash(first ,last),
                    'score': float(score)
                }
                res = self.session.post('https://api.bybitcoinsweeper.com/api/games/win', json=game_data, headers=self.headers)
                if res.status_code == 201:
                    self.info["score"] += score
                    self.log(f"Game Status: WIN","SUCCESS")
                elif res.status_code == 401:
                    self.log('Token expired, need to log in again', "ERROR")
                    return False
                else:
                    self.log(f"An Error Occurred With Code {res.status_code}", 'ERROR')
                self.wait(5)
                return True
            except requests.RequestException:
                self.log('Too Many Requests, Please Wait', 'WARNING')
                self.wait(60)
                return False
    
    def score_lose(self):
            try:
                min_game_time = 70
                max_game_time = 120
                game_time = random.randint(min_game_time, max_game_time)
                playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
                if "message" in playgame:
                    if("expired" in playgame["message"]):
                        self.log("Query Expired Sir", "ERROR")
                        return False
                gameid = playgame["id"]
                rewarddata = playgame["rewards"]
                started_at = playgame["createdAt"]
                userdata = self.userinfo()
                self.log(f"Total Score: {userdata['score']}","SUCCESS")
                unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
                self.log(f"Starting game {gameid}. Play time: {game_time} seconds", 'INFO')
                self.wait(game_time)
                game_data = {
                    "bagCoins": rewarddata["bagCoins"],
                    "bits": rewarddata["bits"],
                    "gifts": rewarddata["gifts"],
                    "gameId": gameid
                }
                res = self.session.post('https://api.bybitcoinsweeper.com/api/games/lose', json=game_data, headers=self.headers)
                if res.status_code == 201:
                    self.log(f"Game Status: LOSEEEEEEEE","ERROR")
                elif res.status_code == 401:
                    self.log('Token expired, need to log in again', "ERROR")
                    return False
                else:
                    self.log(f"An Error Occurred With Code {res.status_code}", 'ERROR')
                self.wait(5)
                return True
            except requests.RequestException:
                self.log('Too Many Requests, Please Wait', 'WARNING')
                self.wait(60)
                return False
    
    def score(self):
        for i in track(range(3), description="Playing games..."):
            try:
                is_win = random.random() < float(0.8)
                if(is_win):
                    if not self.score_win():
                        return False
                else:
                    if not self.score_lose():
                        return False
            except Exception as e:
                print(e)
                return False
        return True
                
    def add_query(self):
        query = animated_input("Enter the query to add: ")
        with open('data.txt', 'a') as f:
            f.write(query + '\n')
        self.log("Query added successfully!", "SUCCESS")

    def add_proxy(self):
        proxy = animated_input("Enter the proxy to add: ")
        with open('proxy.txt', 'a') as f:
            f.write(proxy + '\n')
        self.log("Proxy added successfully!", "SUCCESS")

    def reset_query(self):
        open('data.txt', 'w').close()
        self.log("Query file reset successfully!", "SUCCESS")

    def reset_proxy(self):
        open('proxy.txt', 'w').close()
        self.log("Proxy file reset successfully!", "SUCCESS")

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        animate_banner()
        animate_header_footer()
        
        while True:
            console = Console()
            menu_table = Table(show_header=False, box=ROUNDED, border_style="cyan", width=60)
            menu_table.add_row(Rule(style="bold red"))
            menu_table.add_row("[bold red]===== HACKER'S MENU =====[/bold red]")
            menu_table.add_row(Rule(style="bold red"))
            menu_table.add_row("[green]1. ADD query[/green]")
            menu_table.add_row("[green]2. add Proxy[/green]")
            menu_table.add_row("[green]3. reset Query Database[/green]")
            menu_table.add_row("[green]4. reset Proxy Network[/green]")
            menu_table.add_row("[green]5. bybit start Hack[/green]")
            menu_table.add_row("[red]6. Abort Mission[/red]")
            menu_table.add_row(Rule(style="bold red"))
            
            console.print(Panel(Align.center(menu_table), border_style="cyan", box=ROUNDED, width=60))
            
            choice = animated_input("[yellow]Enter your command: [/yellow]")
            
            if choice == '1':
                self.add_query()
            elif choice == '2':
                self.add_proxy()
            elif choice == '3':
                self.reset_query()
            elif choice == '4':
                self.reset_proxy()
            elif choice == '5':
                self.start_process()
            elif choice == '6':
                console.print(Panel("[red]Mission aborted. Exiting system...[/red]", border_style="red", width=60))
                sys.exit(0)

    def start_process(self):
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        with open(data_file, 'r', encoding='utf8') as f:
            data = [line.strip() for line in f if line.strip()]

        while True:
            proxies = [line.strip() for line in open('proxy.txt') if line.strip()]
            with Live(auto_refresh=False) as live:
                for i, init_data in enumerate(data):
                    proxy = proxies[(i - 1) % len(proxies)] if proxies else None
                    if proxy:
                        self.session.proxies.update({'http': proxy, 'https': proxy})
                    decoded = url_decode(init_data)
                    finaldat = (url_decode(decoded))
                    user_data = json.loads(finaldat.split('user=')[1].split('&')[0])
                    live.update(Panel(f"Processing accounts... {i+1}/{len(data)}"), refresh=True)
                    self.log(f"========== Infiltrating Account {i + 1} | {user_data['first_name']} ==========", 'INFO')
                    self.log(f"Breaching security for account {user_data['id']}...", 'INFO')
                    login_result = self.login(init_data)
                    if login_result["success"]:
                        self.log('Access granted!', "SUCCESS")
                        game_result = self.score()
                        if not game_result:
                            self.log('Security breach detected. Switching to next target.', 'WARNING')
                            continue
                        user_info = self.userinfo()
                        self.log(f"Final Score: {user_info['score'] + user_info['scoreFromReferrals']}", "SUCCESS")
                    else:
                        self.log(f"Infiltration failed! {login_result['error']}", 'ERROR')

                    if i < len(data) - 1:
                        self.wait(3)

            self.wait(3)

if __name__ == '__main__':
    client = ByBit()
    try:
        client.main()
    except Exception as err:
        print(str(err))
        sys.exit(1)
