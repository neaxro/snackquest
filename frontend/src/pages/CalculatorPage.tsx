import { Form, Row, Col, InputGroup } from "react-bootstrap";
import { useEffect, useState } from "react";
import { getMachines } from "../services/SnackquestApi";
import { availableTargetFunctions } from "../types/TargetFunction";

function CalculatorPage() {
  const [machines, setMachines] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState(machines[0]);
  const [selectedTargetFunction, setSelectedTargetFunction] = useState(
    availableTargetFunctions[0]
  );

  useEffect(() => {
    getMachines()
      .then((res) => {
        console.log(res);
        const fetched_machines = res.data;
        setMachines(fetched_machines);
        setSelectedMachine(fetched_machines[0]);
      })
      .catch((error) => console.log(error));
  }, []);

  const handleMachineChange: React.ChangeEventHandler<HTMLSelectElement> = (
    e
  ) => {
    const selected = e.target.value;
    const machine = machines.find((m) => m === selected);
    if (machine) {
      setSelectedMachine(machine);
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

  return (
    <Form>
      <Row>
        <Col className="col-12 col-md-6 col-xl-4">
          <Form.Group className="mb-3" controlId="budget">
            <Form.Label>Budget</Form.Label>
            <InputGroup>
              <InputGroup.Text id="basic-addon1">JMF</InputGroup.Text>
              <Form.Control type="number" min={0} max={15000} step={0} />
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
                value={selectedTargetFunction.display_name}
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
      <p>Selected tf: {selectedTargetFunction.param_name}</p>
      <p>Selected machine: {selectedMachine}</p>
    </Form>
  );
}

export default CalculatorPage;
