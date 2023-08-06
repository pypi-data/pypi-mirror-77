# target-mysql :rocket: :boom:

A [singer.io](https://www.singer.io/) target implementation for MySQL. Because some of us still have to deal with a MySQL data warehouse.

**Under active development like there's no code a barely a roadmap for now**

## Roadmap

- [ ] MySQL connection from config file setup
- [ ] Record message handling
  - [ ] Assert JSON structure
  - [ ] Assert `"schema"` field maps internal known schemas structure
  - [ ] Insert SQL statements
- [ ] Schema message handling
  - [ ] Assert JSON structure
  - [ ] Create table if not exists SQL statements
- [ ] State message handling
  - [ ] Assert JSON structure
  - [ ] Emit state to stdout
