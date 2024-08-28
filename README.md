# Raspberry Pi MiFare Scanner
## A Raspberry Pi MiFare scanner that records scans to a custom MS SQL Database
Files and documentation lives here: https://github.com/queenmargarets/rpi-scan
### Parts List
* Raspberry Pi 4
* Raspberry Pi PoE+ Hat
* RFID-RC522
* <a href="https://thepihut.com/products/miniature-5v-cooling-fan-for-raspberry-pi-and-other-computers">30mm 5v Fan</a>
* Red LED
* 330 ohm resistor
* 3.3v buzzer
* <a href="https://www.adafruit.com/product/2310">AdaFruit Perma Proto Hat</a>
* <a href="https://thepihut.com/products/4-40-pin-pin-extra-tall-header-push-fit-version-poe-hat-set">4 + 40 Pin Push-Fit Extra Tall Header Set for PoE HATs</a>
* <a href="https://cpc.farnell.com/camdenboss/bim2005-15-blk-blk/abs-box-with-lid-black-150x80x50mm/dp/EN55082">Box to fit it in</a>

### Wiring Diagram
<img src="qm-rpi-scan Proto Hat Wiring_bb.png" alt="Wiring diagram for the Raspberry Pi MiFare Scanner" width="75%" height="75%" />

### MS SQL Database Installation
Follow these steps to prepare your MS SQL Database:
1. Run the **rpi-scan-create-db.sql** file on your MS SQL Server
2. In your newly created database, create a new View called **VwADSIUsers** and paste the contents of **rpi-scan-vwadsiusers.sql** in for it's query
3. Create a new login for your server and grant them db-owner role for your newly created database
### Raspberry Pi OS Installation
This is designed to be run from the PiServer setup. First you need to clone the latest **Raspberry Pi OS Lite** on your PiServer. From the PiServer Software tab, open a root shell to your new OS and then follow these steps:
1. Run raspi-config:
```shell
raspi-config
```
2. In the **5 Interfacing Options** menu, enable SPI and SSH
3. Exit raspi-config
4. Install git
```shell
apt install git -y
```
5. Clone this Git Repo:
```shell
git clone https://github.com/queenmargarets/rpi-scan.git
```
6. Move into the repo directory:
```shell
cd rpi-scan
```
7. Run the **setup.sh** script:
```shell
./setup.sh
```
8. Copy **config-dist.py** to **config.py** and open it for editing
```shell
cp config-dist.py config.py
nano config.py
```
9. Enter the details required to connect to your database and save **config.py**

Your PiServer OS image should now be ready to go. Add your Raspberry Pi Scanner clients to your PiServer and assign them the newly setup OS.
