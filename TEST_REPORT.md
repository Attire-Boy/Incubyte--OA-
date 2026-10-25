# Test report

Generated 24 October 2026. Re-create it with the commands in the README's "Running the tests" section.

| Suite | Tool | Result | Line coverage |
|---|---|---|---|
| Backend (FastAPI) | pytest + pytest-cov | **100 passed**, 0 failed | **99%** |
| Frontend (React) | Vitest + Testing Library | **23 passed**, 0 failed | 86.41% statements (files under test) |

## Backend

```
tests/api/test_auth_api.py::TestRegister::test_register_returns_201_with_user_and_token PASSED
tests/api/test_auth_api.py::TestRegister::test_register_never_returns_password_or_hash PASSED
tests/api/test_auth_api.py::TestRegister::test_register_normalises_email_case PASSED
tests/api/test_auth_api.py::TestRegister::test_duplicate_email_returns_409 PASSED
tests/api/test_auth_api.py::TestRegister::test_short_password_returns_422 PASSED
tests/api/test_auth_api.py::TestRegister::test_invalid_email_returns_422 PASSED
tests/api/test_auth_api.py::TestRegister::test_blank_name_returns_422 PASSED
tests/api/test_auth_api.py::TestRegister::test_configured_admin_email_registers_as_admin PASSED
tests/api/test_auth_api.py::TestLogin::test_login_with_valid_credentials_returns_token PASSED
tests/api/test_auth_api.py::TestLogin::test_login_with_wrong_password_returns_401 PASSED
tests/api/test_auth_api.py::TestLogin::test_login_with_unknown_email_returns_401 PASSED
tests/api/test_auth_api.py::TestLogin::test_login_error_message_does_not_reveal_which_field_was_wrong PASSED
tests/api/test_auth_api.py::TestCurrentUser::test_me_returns_current_user PASSED
tests/api/test_auth_api.py::TestCurrentUser::test_me_without_token_returns_401 PASSED
tests/api/test_auth_api.py::TestCurrentUser::test_me_with_invalid_token_returns_401 PASSED
tests/api/test_auth_api.py::TestCurrentUser::test_token_for_user_that_no_longer_exists_returns_401 PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_decreases_quantity_by_one PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_accepts_explicit_quantity PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_is_persisted PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_out_of_stock_returns_409 PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_more_than_stock_returns_409_and_keeps_stock PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_zero_units_returns_422 PASSED
tests/api/test_inventory_api.py::TestPurchase::test_purchase_unknown_vehicle_returns_404 PASSED
tests/api/test_inventory_api.py::TestPurchase::test_admin_can_also_purchase PASSED
tests/api/test_inventory_api.py::TestRestock::test_admin_can_restock PASSED
tests/api/test_inventory_api.py::TestRestock::test_regular_user_cannot_restock PASSED
tests/api/test_inventory_api.py::TestRestock::test_restock_requires_positive_quantity PASSED
tests/api/test_inventory_api.py::TestRestock::test_restock_requires_a_body PASSED
tests/api/test_inventory_api.py::TestRestock::test_restock_unknown_vehicle_returns_404 PASSED
tests/api/test_inventory_api.py::TestRestock::test_restock_makes_sold_out_vehicle_purchasable_again PASSED
tests/api/test_inventory_api.py::TestHealth::test_health_endpoint_is_public PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[get-/api/vehicles] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[post-/api/vehicles] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[get-/api/vehicles/search] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[get-/api/vehicles/1] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[put-/api/vehicles/1] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[delete-/api/vehicles/1] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[post-/api/vehicles/1/purchase] PASSED
tests/api/test_vehicles_api.py::TestAuthenticationRequired::test_every_vehicle_endpoint_requires_a_token[post-/api/vehicles/1/restock] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_admin_can_create_vehicle PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_regular_user_cannot_create_vehicle PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override0] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override1] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override2] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override3] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override4] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_invalid_payload_returns_422[override5] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_missing_required_field_returns_422[make] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_missing_required_field_returns_422[model] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_missing_required_field_returns_422[category] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_missing_required_field_returns_422[price] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_missing_required_field_returns_422[quantity] PASSED
tests/api/test_vehicles_api.py::TestCreateVehicle::test_text_fields_are_trimmed PASSED
tests/api/test_vehicles_api.py::TestListAndGet::test_list_returns_all_vehicles PASSED
tests/api/test_vehicles_api.py::TestListAndGet::test_list_is_empty_when_no_vehicles PASSED
tests/api/test_vehicles_api.py::TestListAndGet::test_get_single_vehicle PASSED
tests/api/test_vehicles_api.py::TestListAndGet::test_get_unknown_vehicle_returns_404 PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_by_make PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_by_model PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_by_category PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_by_min_price PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_by_max_price PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_with_no_filters_returns_everything PASSED
tests/api/test_vehicles_api.py::TestSearch::test_search_with_no_matches_returns_empty_list PASSED
tests/api/test_vehicles_api.py::TestSearch::test_inverted_price_range_returns_400 PASSED
tests/api/test_vehicles_api.py::TestSearch::test_negative_price_returns_422 PASSED
tests/api/test_vehicles_api.py::TestUpdateVehicle::test_admin_can_partially_update_vehicle PASSED
tests/api/test_vehicles_api.py::TestUpdateVehicle::test_regular_user_cannot_update_vehicle PASSED
tests/api/test_vehicles_api.py::TestUpdateVehicle::test_update_unknown_vehicle_returns_404 PASSED
tests/api/test_vehicles_api.py::TestUpdateVehicle::test_update_with_invalid_value_returns_422 PASSED
tests/api/test_vehicles_api.py::TestDeleteVehicle::test_admin_can_delete_vehicle PASSED
tests/api/test_vehicles_api.py::TestDeleteVehicle::test_regular_user_cannot_delete_vehicle PASSED
tests/api/test_vehicles_api.py::TestDeleteVehicle::test_delete_unknown_vehicle_returns_404 PASSED
tests/unit/test_security.py::TestPasswordHasher::test_hash_is_not_the_plain_password PASSED
tests/unit/test_security.py::TestPasswordHasher::test_verify_accepts_correct_password PASSED
tests/unit/test_security.py::TestPasswordHasher::test_verify_rejects_wrong_password PASSED
tests/unit/test_security.py::TestPasswordHasher::test_same_password_produces_different_hashes PASSED
tests/unit/test_security.py::TestTokenService::test_round_trip_returns_subject PASSED
tests/unit/test_security.py::TestTokenService::test_expired_token_is_rejected PASSED
tests/unit/test_security.py::TestTokenService::test_token_signed_with_other_secret_is_rejected PASSED
tests/unit/test_security.py::TestTokenService::test_garbage_token_is_rejected PASSED
tests/unit/test_vehicle_service.py::TestCreateAndRead::test_create_assigns_an_id PASSED
tests/unit/test_vehicle_service.py::TestCreateAndRead::test_get_unknown_vehicle_raises_not_found PASSED
tests/unit/test_vehicle_service.py::TestCreateAndRead::test_list_all_returns_every_vehicle PASSED
tests/unit/test_vehicle_service.py::TestUpdateAndDelete::test_update_changes_only_supplied_fields PASSED
tests/unit/test_vehicle_service.py::TestUpdateAndDelete::test_update_unknown_vehicle_raises_not_found PASSED
tests/unit/test_vehicle_service.py::TestUpdateAndDelete::test_delete_removes_vehicle PASSED
tests/unit/test_vehicle_service.py::TestPurchase::test_purchase_decrements_quantity_by_one_by_default PASSED
tests/unit/test_vehicle_service.py::TestPurchase::test_purchase_multiple_units PASSED
tests/unit/test_vehicle_service.py::TestPurchase::test_purchase_more_than_stock_raises_and_keeps_stock PASSED
tests/unit/test_vehicle_service.py::TestPurchase::test_purchase_out_of_stock_raises PASSED
tests/unit/test_vehicle_service.py::TestPurchase::test_purchase_unknown_vehicle_raises_not_found PASSED
tests/unit/test_vehicle_service.py::TestRestock::test_restock_increments_quantity PASSED
tests/unit/test_vehicle_service.py::TestRestock::test_restock_unknown_vehicle_raises_not_found PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_search_by_make_is_case_insensitive PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_search_by_partial_model PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_search_by_category PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_search_by_price_range_is_inclusive PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_search_combines_filters PASSED
tests/unit/test_vehicle_service.py::TestSearch::test_inverted_price_range_raises_validation_error PASSED
```

### Coverage

```
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
app/__init__.py                              0      0   100%
app/core/__init__.py                         0      0   100%
app/core/config.py                          19      0   100%
app/core/database.py                        15      0   100%
app/core/exceptions.py                      10      0   100%
app/core/security.py                        33      3    91%
app/dependencies.py                         36      0   100%
app/main.py                                 38      1    97%
app/models.py                               29      0   100%
app/repositories/__init__.py                 0      0   100%
app/repositories/user_repository.py         15      0   100%
app/repositories/vehicle_repository.py      44      0   100%
app/routers/__init__.py                      0      0   100%
app/routers/auth.py                         15      0   100%
app/routers/vehicles.py                     30      0   100%
app/schemas.py                              68      0   100%
app/services/__init__.py                     0      0   100%
app/services/auth_service.py                33      0   100%
app/services/vehicle_service.py             37      0   100%
------------------------------------------------------------
TOTAL                                      422      4    99%
```

`app/seed.py` (developer data-seeding script) is excluded from coverage via `.coveragerc`.

## Frontend

```
✓ src/pages/LoginPage.test.jsx > LoginPage > logs in, stores the token and goes to the dashboard 444ms
✓ src/pages/LoginPage.test.jsx > LoginPage > shows the server error when credentials are wrong 254ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > shows make, model, price and stock 60ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > calls onPurchase with the vehicle when Purchase is clicked 172ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > disables Purchase when quantity is zero 14ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > disables Purchase while a purchase is in flight 11ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > hides admin controls for regular users 9ms
✓ src/components/VehicleCard.test.jsx > VehicleCard > shows admin controls and wires them up for admins 83ms
✓ src/components/VehicleForm.test.jsx > VehicleForm > submits typed, numeric values for a new vehicle 426ms
✓ src/components/VehicleForm.test.jsx > VehicleForm > blocks submission and explains when required fields are missing 42ms
✓ src/components/VehicleForm.test.jsx > VehicleForm > rejects a non-positive price 38ms
✓ src/components/VehicleForm.test.jsx > VehicleForm > pre-fills values and says "Save changes" when editing 28ms
✓ src/api/client.test.js > apiRequest > sends JSON and returns the parsed body 5ms
✓ src/api/client.test.js > apiRequest > attaches the bearer token when one is stored 2ms
✓ src/api/client.test.js > apiRequest > omits Authorization when there is no token 1ms
✓ src/api/client.test.js > apiRequest > returns null for 204 No Content 0ms
✓ src/api/client.test.js > apiRequest > throws ApiError with the server detail on failure 1ms
✓ src/api/client.test.js > apiRequest > flattens FastAPI validation errors into a readable message 0ms
✓ src/api/client.test.js > apiRequest > builds query strings and skips empty params 0ms
✓ src/utils/format.test.js > formatPrice > formats whole dollars with separators 2ms
✓ src/utils/format.test.js > stockLabel > describes sold out, last unit and plural stock 1ms
✓ src/utils/format.test.js > filters > detects whether any server-side filter is set 0ms
✓ src/utils/format.test.js > filters > maps UI filters to API search params 1ms
```

### Coverage

```
File              | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
All files         |   86.41 |    83.33 |   77.41 |   85.61 |                   
 api              |   77.55 |    87.87 |   52.38 |    75.6 |                   
  client.js       |   94.59 |    90.62 |    90.9 |   96.55 | 34                
  endpoints.js    |      25 |        0 |      10 |      25 | 5,7,11-19         
 components       |   93.75 |    84.28 |   95.23 |   91.83 |                   
  AppHeader.jsx   |   33.33 |       60 |      50 |   33.33 | 12-14             
  VehicleCard.jsx |     100 |       90 |     100 |     100 | 25-33             
  VehicleForm.jsx |   95.91 |    84.44 |     100 |   94.44 | 21,88             
 context          |      70 |       50 |      70 |      72 |                   
  AuthContext.jsx |      70 |       50 |      70 |      72 | 9-12,26-28,37     
 utils            |   95.23 |    76.47 |     100 |     100 |                   
  format.js       |   95.23 |    76.47 |     100 |     100 | 26-29             
```
