python3 -m venv venv
source venv/bin/activate

sudo apt remove xtrx-dkms
pip install pyrtlsdr

python3 VHF.py