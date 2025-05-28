import { Form, Row, Col, InputGroup, Stack, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import { getMachines, getInventory } from "../services/SnackquestApi";
import { availableTargetFunctions } from "../types/TargetFunction";
import { Snack } from "../types/Snack";
import ToggleSnackButton from "../components/calculator/ToggleSnackButton";
import SnackCard from "../components/calculator/SnackCard";

function CalculatorPage() {
  const [machines, setMachines] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState(machines[0]);
  const [selectedTargetFunction, setSelectedTargetFunction] = useState(
    availableTargetFunctions[0]
  );
  const [snacks, setSnacks] = useState([]);
  const [selectedSnacks, setSelectedSnacks] = useState<Snack[]>([]);
  const [validated, setValidated] = useState(false);
  const [snacksValid, setSnacksValid] = useState(true);

  useEffect(() => {
    getMachines()
      .then((res) => {
        console.log(res);
        const fetched_machines = res.data;
        setMachines(fetched_machines);
        setSelectedMachine(fetched_machines[0]);
        loadInventory(fetched_machines[0]);
      })
      .catch((error) => console.log(error));
  }, []);

  const loadInventory = (machineName: string) => {
    getInventory(machineName).then((res) => {
      console.log(res);
      const fetched_snacks = res.data;
      setSnacks(fetched_snacks["items"]);
    });
  };

  const handleMachineChange: React.ChangeEventHandler<HTMLSelectElement> = (
    e
  ) => {
    const selected = e.target.value;
    const machine = machines.find((m) => m === selected);
    if (machine) {
      setSelectedMachine(machine);
      loadInventory(machine);
      setSelectedSnacks([]);
      setSnacks([]);
    }
  };

  const handleTargetFunctionChange: React.ChangeEventHandler<
    HTMLSelectElement
  > = (e) => {
    const selected = e.target.value;
    const tf = availableTargetFunctions.find(
      (tf) => tf.param_name === selected
    );
    if (tf) {
      setSelectedTargetFunction(tf);
    }
  };

  const handleToggleChange = (snack: Snack, selected: boolean) => {
    if (selected) {
      if (!selectedSnacks.some((s) => s.name === snack.name)) {
        setSelectedSnacks([...selectedSnacks, { ...snack }]);
      }
    } else {
      const newList = selectedSnacks.filter((s) => s.name !== snack.name);
      setSelectedSnacks(newList);
    }
  };

  const updateSnackDesired = (index: number, newDesired: number) => {
    setSelectedSnacks((prevSnacks) => {
      const updated = [...prevSnacks];
      updated[index] = { ...updated[index], desired: newDesired };
      return updated;
    });
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const form = event.currentTarget as HTMLFormElement;

    const isSnacksValid = selectedSnacks.length > 0;
    setSnacksValid(isSnacksValid);

    if (form.checkValidity() === false || !isSnacksValid) {
      event.stopPropagation();
    } else {
      console.log("Submit pressed with:", {
        selectedSnacks,
        selectedTargetFunction,
        selectedMachine,
      });
    }

    setValidated(true);
  };

  return (
    <Form noValidate validated={validated} onSubmit={handleSubmit}>
      <Row>
        <Col className="col-12 col-md-6 col-xl-4">
          <Form.Group className="mb-3" controlId="budget">
            <Form.Label>Budget</Form.Label>
            <InputGroup>
              <InputGroup.Text id="basic-addon1">JMF</InputGroup.Text>
              <Form.Control
                required
                type="number"
                min={0}
                max={15000}
                step={0}
              />
              <Form.Control.Feedback type="invalid">
                Please provide your balance. (max 15000)
              </Form.Control.Feedback>
            </InputGroup>
          </Form.Group>
        </Col>

        <Col className="col-12 col-md-6 col-xl-4">
          <Form.Group className="mb-3" controlId="target_function">
            <Form.Label>Target function</Form.Label>
            <InputGroup>
              <Form.Select
                aria-label="Floating label select example"
                onChange={handleTargetFunctionChange}
                value={selectedTargetFunction.param_name}
              >
                {availableTargetFunctions.map((tf) => (
                  <option key={tf.param_name} value={tf.param_name}>
                    {tf.display_name}
                  </option>
                ))}
              </Form.Select>
            </InputGroup>
            <Form.Text className="text-muted">
              {selectedTargetFunction.description}
            </Form.Text>
          </Form.Group>
        </Col>

        <Col className="col-12 col-md-6 col-xl-4">
          <Form.Group className="mb-3" controlId="machine_name">
            <Form.Label>Machine</Form.Label>
            <Form.Select
              aria-label="Floating label select example"
              onChange={handleMachineChange}
              value={selectedMachine}
            >
              {machines.map((machine) => (
                <option key={machine} value={machine}>
                  {machine}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>

      <Form.Group className="mb-3" controlId="snacks_selection">
        <Form.Label>
          <h5>Available snacks</h5>
        </Form.Label>
        <p>Only selected snacks will be included in the calculation.</p>
        <Stack gap={3} direction="horizontal" className="col-12 flex-wrap">
          {snacks.map((snack: Snack, index) => (
            <ToggleSnackButton
              key={index}
              snack={snack}
              onToggleChanged={(selected) =>
                handleToggleChange(snack, selected)
              }
            />
          ))}
        </Stack>

        {!snacksValid && validated && (
          <div className="text-danger mt-1">
            Please select at least one snack to proceed.
          </div>
        )}
      </Form.Group>

      <h5 className="mt-4">Selected snacks</h5>
      <Stack gap={2} direction="horizontal" className="flex-wrap col-12">
        {selectedSnacks.map((snack, index) => (
          <SnackCard
            key={snack.name}
            snack={snack}
            onDesiredChange={(newDesired) =>
              updateSnackDesired(index, newDesired)
            }
          />
        ))}
      </Stack>

      <Button
        className="mt-5"
        variant="primary"
        type="submit"
        disabled={selectedSnacks.length === 0}
      >
        Calculate
      </Button>
    </Form>
  );
}

export default CalculatorPage;
