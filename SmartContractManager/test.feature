Feature: contract test
  Scenario: run contract
    Given input transaction
      When implements transaction
      Then contract make correct state_trace
