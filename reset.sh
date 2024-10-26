rm token
lxc image delete $(lxc image list --format csv -c "l")
lxc delete --force $(lxc list --format csv -c "n")
