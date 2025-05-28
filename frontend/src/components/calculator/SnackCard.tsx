import { Snack } from "../../types/Snack";
import { Card, ListGroup, ButtonGroup, Button } from "react-bootstrap";
import { PlusCircleFill, DashCircleFill } from "react-bootstrap-icons";

type Props = {
  snack: Snack;
  onDesiredChange: (newDesired: number) => void;
};

function SnackCard({ snack, onDesiredChange }: Props) {
  return (
    <Card className="col-12 col-md-5 col-lg-3">
      <Card.Body>
        <div className="d-flex justify-content-between">
          <div>
            <b>{snack.name}</b>
          </div>
          <div>{snack.price} JMF</div>
        </div>
      </Card.Body>
      <ListGroup className="list-group-flush">
        <ListGroup.Item>
          <div className="d-flex justify-content-between align-items-center">
            <span className="pe-2">Minimum Amount</span>
            <ButtonGroup size="sm">
              <Button
                variant="outline-secondary"
                onClick={() =>
                  snack.desired > 0 && onDesiredChange(snack.desired - 1)
                }
              >
                <DashCircleFill />
              </Button>
              <Button variant="light" disabled style={{ minWidth: 50 }}>
                {snack.desired ?? 0}
              </Button>
              <Button
                variant="outline-secondary"
                onClick={() =>
                  snack.desired < 25 && onDesiredChange(snack.desired + 1)
                }
              >
                <PlusCircleFill />
              </Button>
            </ButtonGroup>
          </div>
        </ListGroup.Item>
      </ListGroup>
    </Card>
  );
}

export default SnackCard;
