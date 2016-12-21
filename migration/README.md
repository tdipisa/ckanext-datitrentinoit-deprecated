
##PREPARING THE SYSTEM FOR DCAT_AP-IT

This ckanext-datitrentinoit has been updated to integrate the old version of this extension with ckanext-dcatapit:

	Follow the steps below only the first time you prepare the system for installing the ckanext-dcatapit.

1. Backup the DB ckan:
	
		su postgres

		pg_dump -U postgres -i ckan > ckan.dump
	
2. Run the SQL migration script to update DB tables:

		su postgres

		psql -U postgres -d ckan -f /usr/local/data_loc/src/ckanext-datitrentinoit/migration/sql/migration.sql
	
3. Upgrade the python setuptools version installed (only if ckan version < 2.5):

		pip install --upgrade setuptools

4. Install the ckanext-dcat extension:

		. /usr/local/app_loc/geosolutions/bin/activate

		cd /usr/local/data_loc/src

		git clone https://github.com/ckan/ckanext-dcat.git

		cd ckanext-dcat

		pip install -e .

		pip install -r requirements.txt

5. Install the ckanext-dcatapit following the steps reported [here](https://github.com/geosolutions-it/ckanext-dcatapit#installation):

	**Ingore the point number 1**
	
		Pay attention that in the datitrentinoit system the paths below change from ones reported in the ckanext-dcatapit installation README:
		
			. /usr/lib/ckan/default/bin/activate -> . /usr/local/app_loc/geosolutions/bin/activate
			
			/etc/ckan/default/production.ini     -> /usr/local/app_loc/geosolutions/conf/production.ini
			
			/usr/lib/ckan/default/src            -> /usr/local/data_loc/src
		
6. Update the ckanext-multilang extension:

		. /usr/local/app_loc/geosolutions/bin/activate

		cd /usr/local/data_loc/src/ckanext-multilang
		
		git checkout master

		git pull 

		pip install -e .
		
7. Uninstall the old ckanext-harvest-tn extenstion (now available in the new ckanext-datitrentinoit):

		. /usr/local/app_loc/geosolutions/bin/activate
		
		cd /usr/local/data_loc/src/ckanext-harvest-tn
		
		pip uninstall .
		
		rm -rf /usr/local/data_loc/src/ckanext-harvest-tn
	
8. Update the ckanext-datitrentinoit extension:

		. /usr/local/app_loc/geosolutions/bin/activate

		cd /usr/local/data_loc/src/ckanext-datitrentinoit

		git pull 

		git checkout dcatapit

		pip install -e .
	
	- Update the `/usr/local/app_loc/geosolutions/conf/production.ini` file removing the property below:
	
			ckan.i18n_directory
	
9. Restart CKAN

10. Rebuild the Solr indexes:

		. /usr/local/app_loc/geosolutions/bin/activate

		paster --plugin=ckan search-index rebuild  -c /usr/local/app_loc/geosolutions/conf/production.ini
