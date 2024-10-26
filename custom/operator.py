import kopf
import subprocess

# LXDコンテナを作成するための関数
def create_lxd_container(name, image):
    command = ["lxc", "launch", image, name]
    subprocess.run(command, check=True)

# LXDコンテナを削除するための関数
def delete_lxd_container(name):
    command = ["lxc", "delete", name, "--force"]
    subprocess.run(command, check=True)

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
