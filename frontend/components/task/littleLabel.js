import { getColor } from '../label/row';

const LittleLabel = ({ name, color }) => {
  const style = {
    backgroundColor: color,
    // padding: '7px',
    // borderRadius: '25px',
    // height: '40px',
    alignSelf: 'center',
    color: getColor(color)
  };
  return (
    <>
      {name && (
        <span className='ml-3 badge badge-pill' style={style}>
          {name}
        </span>
      )}
    </>
  );
};

export default LittleLabel;
