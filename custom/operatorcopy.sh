#!/bin/bash

# ファイルのパス
LXD_CLUSTERFILE="lxdclusterfile"
OPERATOR_FILE="operatorssh2.py"

rm ./lxdclusterfile
rm ./operatorssh2.py
cp operatorssh.py operatorssh2.py
cp ../lxdclusterfile .

# lxdclusterfile の一行目を読み取り、変数に格納
read -r HOST_NAME IP_ADDRESS USER PASSWORD < <(head -n 1 "$LXD_CLUSTERFILE")

# operatorssh2.py の内容を置き換え
sed -i "s/xxxxxx/$IP_ADDRESS/g" "$OPERATOR_FILE"
sed -i "s/root/$USER/g" "$OPERATOR_FILE"
sed -i "s/passwordgen/$PASSWORD/g" "$OPERATOR_FILE"

echo "置き換えが完了しました。"
