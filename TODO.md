# Todos

- [ ] Need a way to keep track of all objects that exist for a particular type and all sub-types
  - there can't be a subtype or an object of a type, to remove that type
  - might be best to have a TermManager
  - best solution might be doing a search over
  - if you remove a type from an action predicate
  - solution 1: fail unless theres no instances of that type. we want 1-step transformations
  - solution 2: replace all current instances of that type with the parent type or object