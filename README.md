

## Features  
| Feature                                                     | Supported  |
|---------------------------------------------------------------|:----------------:|
| Multithreading                                                |        ✅        |
| Proxy binding to session                                      |        ✅        |
| Auto ref                                                      |        ✅        |
| Auto play game                                                |        ✅        |
| Support for pyrogram Query                                    |        ✅        |

# Termux manual installation
```
> pkg update && pkg upgrade -y
> pkg install python rust git -y
> git clone https://github.com/mosiburpaik/coinsweeper.git
> cd Coinsweeper
> pip install -r requirements.txt
> python main.py
```

You can also use arguments for quick start, for example:
```termux
~/Coinsweeper > python main.py --action (1/2)
# Or
~/Coinsweeper > python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session 
```
