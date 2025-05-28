import ToggleButton from "react-bootstrap/ToggleButton";
import { useState } from "react";
import { Snack } from "../../types/Snack";

interface Props {
  snack: Snack;
  onToggleChanged: (selected: boolean) => void;
}

function ToggleSnackButton({ snack, onToggleChanged }: Props) {
  const [checked, setChecked] = useState(false);
  return (
    <ToggleButton
      id={snack.name}
      type="checkbox"
      variant="outline-primary"
      checked={checked}
      value="1"
      onChange={(e) => {
        const newValue = !checked;
        setChecked(newValue);
        onToggleChanged(newValue);
      }}
    >
      {snack.name}
    </ToggleButton>
  );
}

export default ToggleSnackButton;
