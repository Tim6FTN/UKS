import { getColor } from '../label/row';

const LittleLabel = ({ name, color }) => {
  const style = {
    backgroundColor: color,
    padding: '7px',
    borderRadius: '25px',
    color: getColor(color)
  };
  return (
    <>
      {name && (
        <span className='mx-2' style={style}>
          {name}
        </span>
      )}
    </>
  );
};

export default LittleLabel;
