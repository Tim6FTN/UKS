import { useRouter } from "next/router";
import { useState } from "react";
import LabelForm from "./form";

const LabelRow = ({ label, tryDelete, onUpdate }) => {

  const [visible, setVisible] = useState(false)
  const router = useRouter()

  const update = (label) => {
    onUpdate(label);
    setVisible(false);
  }
  return (
    <>
      <tr>
        <td><span className="p-2 rounded" style={{ backgroundColor: label.color, color: getColor(label.color) }}>{label.name}</span></td>
        <td><button className="btn btn-secondary" onClick={() => setVisible(!visible)}>Edit</button></td>
        <td><button className="btn btn-danger" onClick={() => tryDelete(router.query.id, label.id)}>Delete</button></td>
      </tr>
      {visible &&
        <tr>
          <td colSpan={3}>
            <LabelForm label={label} onUpdate={update} />
          </td>
        </tr>
      }
    </>
  )
}

function getColor(hexcolor) {
  hexcolor = hexcolor.replace("#", "");
  var r = parseInt(hexcolor.substr(0, 2), 16);
  var g = parseInt(hexcolor.substr(2, 2), 16);
  var b = parseInt(hexcolor.substr(4, 2), 16);
  var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
  return (yiq >= 128) ? 'black' : 'white';
}

export default LabelRow