import { useEffect, useState } from "react";
import LabelService from "../../../services/labelService";
import LabelForm from "../../../components/label/form";
import LabelRow from "../../../components/label/row";
import Navbar from "../../../components/util/navbar"
import Container from "../../../components/util/container";
import { useRouter } from "next/router";


const Label = () => {
  const emptyLabel = {
    id: null,
    name: "",
    color: "#000000"
  }
  const [label, setLabel] = useState(emptyLabel)
  const [labels, setLabels] = useState([])
  const [labelFormHidden, setLabelFormHidden] = useState(true)
  const router = useRouter()

  useEffect(() => {
    if (router.query.id)
      LabelService.getAll(router.query.id).then(response => setLabels(response.data))
  }, [router.query.id])

  const labelRows = () =>
    labels.map((label, index) =>
      <LabelRow key={index} label={label} tryDelete={tryDelete} onUpdate={onUpdate} />
    )

  const tryDelete = (projectId, labelId) => {
    if (window.confirm("Are you sure you want to delete this Label?"))
      LabelService.remove(projectId, labelId).then(response => setLabels(labels.filter(label => label.id !== labelId)))
  }

  const onCreate = (newLabel) => {
    setLabels([...labels, newLabel])
  }

  const onUpdate = updatedLabel => {
    console.log(updatedLabel)
    setLabels(labels.map(label => (label.id === updatedLabel.id ? { ...updatedLabel } : label)))
  }

  const newLabel = () => {
    setLabel(emptyLabel)
    setLabelFormHidden(!labelFormHidden)
  }
  return (
    <>
      <Navbar />
      <Container>
        <div>
          <h1>LABEL</h1>

          <div>
            <button className="btn btn-success" onClick={() => newLabel()}>
              New label
        </button>
          </div>

          {!labelFormHidden && <LabelForm onCreate={onCreate} label={label} />}

          <table className="table">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Edit</th>
                <th scope="col">Delete</th>
              </tr>
            </thead>
            <tbody>{labelRows()}</tbody>
          </table>
        </div>
      </Container>
    </>
  );
};




export default Label