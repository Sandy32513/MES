# HANDOFF NOTE: A4 (Pipeline) to A5 (HMI)

## What is Done
1. OPC UA tags verified and mapped to Ignition structure: `[default]MES/Machine01/<Tag>`.
2. `Comm_OK` expression tag defined.
3. Database `mes_production_db` accumulating live status intervals and production counts.
4. Color codes established: RUN (#28a745), STOP (#dc3545), IDLE (#ffc107), COMM_LOSS (#6c757d).

## Available Views & Tables for Screen 3
- Table `production_log`: raw records with `recorded_at`, `total_count`, `good_count`, `reject_count`, `cycle_time`, `temperature`.
- View `v_production_by_shift`: shift-wise totals (`machine_id`, `production_date`, `shift_name`, `total_produced`, `good_produced`, `reject_produced`).
- View `v_current_shift`: active shift indicator.
