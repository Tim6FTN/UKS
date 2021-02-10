const Container = props => {
  return (
    <div className="container bg-light p-5 mt-3">
      {props.children}
    </div>
  )
}

export default Container