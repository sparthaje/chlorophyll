
# Configuring a new node

1) Flash Raspbian Buster onto it
	add wpa_supplicant file into bood drive
	add ssh file into boot drive

2) Change the passwords of the nodes
	for both `pi` and `root`

3) Change hostname to chlorophyll-NUMBER

4) Configure ssh for `root`

5) Copy ssh keys to `root@hostname`

6) `ansible-playbook -i hosts configure_nodes.yml`

7) Upload compressed docker images to ~/dockerimages
	look at roles/upload_docker_images/README.md 
	
8) `ansible-playbook -i hosts configure_nodes.yml`

9) Run the individual run_files manually in ~/.config/chlorophyll on the node
