/* updates for package_extra fields */

UPDATE package_extra SET key='holder_name' WHERE key='holder';
UPDATE package_extra SET key='geographical_name' WHERE key='geographical_coverage';
UPDATE package_extra SET key='temporal_start' WHERE key='temporal_coverage_start';
UPDATE package_extra SET key='temporal_end' WHERE key='temporal_coverage_end';
UPDATE package_extra SET key='frequency' WHERE key='update_frequency';
UPDATE package_extra SET key='issued' WHERE key='publication_date';
UPDATE package_extra SET key='modified' WHERE key='revision_date';

/* updates for the package_extra 'frequency' value */

UPDATE package_extra SET value='IRREG' WHERE key='frequency' AND (lower(value)='asneeded' OR lower(value)='se necessario' OR lower(value)='falls erforderlich');

UPDATE package_extra SET value='QUARTERLY' WHERE key='frequency' AND (lower(value)='quarterly' OR lower(value)='quartale' OR lower(value)='vierteljährlich');

UPDATE package_extra SET value='BIWEEKLY' WHERE key='frequency' AND (lower(value)='fortnightly' OR lower(value)='stagionale' OR lower(value)='saisonal');

UPDATE package_extra SET value='ANNUAL' WHERE key='frequency' AND (lower(value)='annually' OR lower(value)='annuale' OR lower(value)='jährlich');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND (lower(value)='estemporaneo' OR lower(value)='' OR lower(value)='');

UPDATE package_extra SET value='BIENNIAL' WHERE key='frequency' AND (lower(value)='biannually' OR lower(value)='biennale' OR lower(value)='zweijährlich');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND (lower(value)='four-monthly' OR lower(value)='quadrimestrale' OR lower(value)='vier-monats');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND (lower(value)='half-yearly' OR lower(value)='semestrale' OR lower(value)='halbjährlich');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND (lower(value)='undefined' OR lower(value)='non definito' OR lower(value)='undefiniert');

UPDATE package_extra SET value='TRIENNIAL' WHERE key='frequency' AND (lower(value)='three-year' OR lower(value)='triennale' OR lower(value)='triennale');

UPDATE package_extra SET value='IRREG' WHERE key='frequency' AND (lower(value)='unplanned' OR lower(value)='non pianificato' OR lower(value)='ungeplant');

UPDATE package_extra SET value='UPDATE_CONT' WHERE key='frequency' AND (lower(value)='continues' OR lower(value)='continua' OR lower(value)='weiter');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND lower(value)='hourly' OR (lower(value)='orario' OR lower(value)='zeit');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND (lower(value)='2013' OR lower(value)='2013' OR lower(value)='2013');

UPDATE package_extra SET value='IRREG' WHERE key='frequency' AND (lower(value)='not expected' OR lower(value)='non previsto' OR lower(value)='nicht zu erwarten');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND (lower(value)='decennial' OR lower(value)='decennale' OR lower(value)='zehnjährig');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND (lower(value)='constant dataset' OR lower(value)='dataset costante' OR lower(value)='konstante-datensatz');

UPDATE package_extra SET value='QUARTERLY' WHERE key='frequency' AND (lower(value)='quarterly' OR lower(value)='trimestrale' OR lower(value)='vierteljährlich');

UPDATE package_extra SET value='OTHER' WHERE key='frequency' AND (lower(value)='quinquennial' OR lower(value)='quinquennale' OR lower(value)='alle fünf Jahre');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND value='';

UPDATE package_extra SET value='MONTHLY' WHERE key='frequency' AND (lower(value)='monthly' OR lower(value)='mensile' OR lower(value)='monatlich');

UPDATE package_extra SET value='WEEKLY' WHERE key='frequency' AND (lower(value)='weekly' OR lower(value)='settimanale' OR lower(value)='wöchentlich');

UPDATE package_extra SET value='DAILY' WHERE key='frequency' AND (lower(value)='daily' OR lower(value)='giornaliero' OR lower(value)='täglich');

UPDATE package_extra SET value='UPDATE_CONT' WHERE key='frequency' AND (lower(value)='continual' OR lower(value)='continuo' OR lower(value)='dauer');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND (lower(value)='notplanned' OR lower(value)='non programmato' OR lower(value)='unprogrammierten');

UPDATE package_extra SET value='IRREG' WHERE key='frequency' AND (lower(value)='irregular' OR lower(value)='irregolare' OR lower(value)='irregulär');

UPDATE package_extra SET value='UNKNOWN' WHERE key='frequency' AND (lower(value)='unknown' OR lower(value)='sconosciuto' OR lower(value)='unbekannt');

/* porting records from custom table to package_multilang */

UPDATE package_multilang SET field_type='package' WHERE field_type='localized';

ALTER TABLE custom_field_table ADD COLUMN field_type text;
UPDATE custom_field_table SET field_type='extra';

INSERT INTO package_multilang (package_id, field, field_type, lang, text) SELECT package_id, field, field_type, lang, text FROM custom_field_table;

UPDATE package_multilang SET field='holder_name' WHERE field='holder';
UPDATE package_multilang SET field='geographical_name' WHERE field='geographical_coverage';
UPDATE package_multilang SET field='temporal_start' WHERE field='temporal_coverage_start';
UPDATE package_multilang SET field='temporal_end' WHERE field='temporal_coverage_end';
UPDATE package_multilang SET field='frequency' WHERE field='update_frequency';
UPDATE package_multilang SET field='issued' WHERE field='publication_date';
UPDATE package_multilang SET field='modified' WHERE field='revision_date';