pip3 install requests
python3 models.py
git add models.json && git -c "user.name=$USER" -c "user.email=$EMAIL" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$USER@github.com/$USER/huawei_devices.git HEAD:models
 
