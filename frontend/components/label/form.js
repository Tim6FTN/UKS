import { useRouter } from "next/router"
import { useState } from "react"
import LabelService from "../../services/labelService"

const LabelForm = (props) => {

  const [label, setLabel] = useState(props.label)
  const router = useRouter()

  const submit = (event) => {
    event.preventDefault();
    if (label.id)
      LabelService.update(router.query.id, label.id, label).then(response => { props.onUpdate(response.data) })
    else {
      LabelService.create(router.query.id, label)
        .then(response => {
          console.log(response.data);
          props.onCreate(response.data);
          setLabel(props.label)
        })
        .catch(error => alert(error))
    }
  }
  return (
    <div>
      <form className="form" onSubmit={submit}>
        <div className="form-row">
          <div className="form-group">
            <input type="text" className="form-control" placeholder="Name" value={label.name} onChange={(event) => setLabel({ ...label, name: event.target.value })} />
          </div>
          <div className="form-group">
            <input style={{ padding: 0, width: 40 }} type="color" className="form-control" value={label.color} onChange={(event) => setLabel({ ...label, color: event.target.value })} />
          </div>
          <div className="form-group">
            <input type="text" className="form-control" value={label.color} onChange={(event) => setLabel({ ...label, color: event.target.value })} />
          </div>
          <div className="form-group">
            <input type="submit" className="btn btn-success" value="Submit" />
          </div>
        </div>
      </form>
    </div >
  )
}

export default LabelForm