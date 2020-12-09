-- Add a new column of the precomputed
-- search text vectors
ALTER TABLE asset
  ADD COLUMN search_vec tsvector;
UPDATE asset
  SET search_vec = to_tsvector(
      coalesce(description, '') || ' ' ||
      status || ' ' ||
      bartdept
  );

ALTER TABLE mpu
  ADD COLUMN search_vec tsvector;
UPDATE mpu
  SET search_vec = to_tsvector(
    name || ' ' ||
    description || ' ' ||
    location || ' ' ||
    sub_location || ' ' ||
    coalesce(accomplishments, '') || ' ' ||
    project_group || ' ' ||
    project_manager
  );

ALTER TABLE work_order
  ADD COLUMN search_vec tsvector;
UPDATE work_order
  SET search_vec = to_tsvector(
      location || ' ' ||
      coalesce(description, '') || ' ' ||
      asset_type || ' ' ||
      bartdept
  );
