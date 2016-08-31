# Installation notes

A log of any unusual steps needed to be taken when deploying the site

## Deployment 2016 08 31

- Seminar models will not port nicely. I get SQL failures on `mysqldump` and DB integrity errors on `loaddata`. Best option is to mysqldump full database but not to include Seminar data. Export seminar data to a fixture with `dumpdata` management command. Upload mysql dump, migrate DB, then import the fixture.
