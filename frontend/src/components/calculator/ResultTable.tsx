import { Alert, Table } from "react-bootstrap";
import { CalculateResult } from "../../types/CalculateResult";

interface Props {
  result: CalculateResult;
  statusCode: number;
}

function ResultTable({ result, statusCode }: Props) {
  if (statusCode === 204) {
    return (
      <Alert className="d-flex align-items-center" variant="danger">
        <div>There is no solution!</div>
      </Alert>
    );
  }
  if (statusCode === 200) {
    return (
      <Table className="table-hover table-bordered">
        <thead className="table-primary">
          <tr>
            <th>Snack</th>
            <th>Count</th>
            <th>Unit price</th>
          </tr>
        </thead>
        <tbody>
          {result.final_items.map((item, index) => (
            <tr>
              <th scope="row">{item.name}</th>
              <td>{item.count}</td>
              <td>{item.unit_price}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="table-primary">
            <td colSpan={3}> </td>
          </tr>
          <tr>
            <th>Total</th>
            <td>{result.total_candies}</td>
            <td>{result.total_cost}</td>
          </tr>
          <tr>
            <th>Remaining</th>
            <td></td>
            <td>{result.budget - result.total_cost}</td>
          </tr>
        </tfoot>
      </Table>
    );
  } else {
    return (
      <Alert className="d-flex align-items-center" variant="warning">
        <div>Something went wrong...</div>
      </Alert>
    );
  }
}

export default ResultTable;
