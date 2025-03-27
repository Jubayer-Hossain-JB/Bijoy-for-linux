# Bijoy For Linux
It's a keyboard engine developed for working with IBus for linux. It includes both Unicode and Classic flavour of Bijoy bangla keyboard layout.
## Installation
### 1. Install Dependencies
Install IBus and Python bindings for your Linux distribution:

#### Debian/Ubuntu-based
```bash
sudo apt install ibus python3-gi gir1.2-ibus-1.0
```
#### Fedora
```bash
sudo dnf install ibus python3-gobject
```
#### Arch/Manjaro
```bash
sudo pacman -S ibus python-gobject
```
### 2. Download 
Just download Install_Bijoy.py only
### 3. Install it
then run 
```bash
sudo python3 ~/downloads/Install_Bijoy.py
```
- Adjust the path to the file and run.
- Run and type your password
### 4. Restart IBus
```bash
sudo ibus restart
```
### 5. Add it from keyboard Settings
You can find the keyboards from ibus preference > add keyboard  > under Bangla Section> Bijoy unicode or Bijoy classic

> [!IMPORTANT]
> This is in development stage
> For now, it is just tested in **Fedora**

