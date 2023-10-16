## Kinescope XBlock

XBlock for embedding Kinescope Videos.

### Local setup

1. Clone this repository into `devstack_root/src/` directory.
1. Add the following to `devstack_root/devstack/options.local.mk`:
	```bash
	# Restart both containers
	edx-restart: lms-restart cms-restart

	# This allows you to install an XBlock in both lms and studio using
	# make install-xblock XBLOCK=problem-builder
	install-xblock:
		for c in lms cms ; do \
			docker exec -it edx.${COMPOSE_PROJECT_NAME}.$$c bash -c \
			'cd /edx/src/$(XBLOCK) && /edx/app/edxapp/venvs/edxapp/bin/pip install -e .' ;   \
		done
		make edx-restart
	```
1. Run `make install-xblock XBLOCK=xblock-kinescope`.

## Usage
1. Go to `Settings -> Advanced Settings` in a specific course within Studio.
1. Add `"kinescope"` to `Advanced Module List` and save.
1. Add `Advanced -> Kinescope` unit to the course.
1. Go to Kinescope dashboard (https://app.kinescope.io/video)
1. Right click on any video and select `Copy Link`
1. Click on the edit button of the XBlock unit and paste the link in `Video Link/URL` field
1. Save the XBlock
