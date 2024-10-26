import kopf
import paramiko


# SSH接続情報
SSH_HOST = "10.171.70.1"  # lxdclusterfileの一行目のIPアドレス
SSH_USER = "root"
SSH_PASSWORD = "hiyiir"  # 適切なパスワードに置き換え


# SSH経由でコマンドを実行する関数
def run_ssh_command(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSH_HOST, username=SSH_USER, hiyiir=SSH_PASSWORD)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            raise Exception(f"Error: {error}")
        return output
    finally:
        client.close()

# LXDコンテナを作成する関数
def create_lxd_container(name, image):
    command = f"lxc launch {image} {name}"
    run_ssh_command(command)

# LXDコンテナを削除する関数
def delete_lxd_container(name):
    command = f"lxc delete {name} --force"
    run_ssh_command(command)

# オペレーターのハンドラで、LXDコンテナを作成
@kopf.on.create('mydomain.com', 'v1', 'lxdcontainers')
def on_create(spec, **kwargs):
    name = spec.get('name')
    image = spec.get('image')

    # LXDコンテナを作成
    if name and image:
        create_lxd_container(name, image)
        return {'message': f"LXD container '{name}' created with image '{image}'."}

# オペレーターのハンドラで、LXDコンテナを削除
@kopf.on.delete('mydomain.com', 'v1', 'lxdcontainers')
def on_delete(spec, **kwargs):
    name = spec.get('name')

    # LXDコンテナを削除
    if name:
        delete_lxd_container(name)
        return {'message': f"LXD container '{name}' deleted."}
