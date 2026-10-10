const Component = () => {
  const cond = true;
  return (
    <div>
      {cond ? (
        <div>A</div>
      ) : (
        <>
          <div>B</div>
        </>
      )}
    </div>
  );
};
