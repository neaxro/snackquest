import { Card } from "react-bootstrap";
import { ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode; // HTML string
}

function InfoCard({ title, children }: Props) {
  return (
    <Card className="card-section mb-3 shadow-lg">
      <Card.Body>
        <Card.Title className="pb-2">{title}</Card.Title>
        <Card.Text>{children}</Card.Text>
      </Card.Body>
    </Card>
  );
}

export default InfoCard;
