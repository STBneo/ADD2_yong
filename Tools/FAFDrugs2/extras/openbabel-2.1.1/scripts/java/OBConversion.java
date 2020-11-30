/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.31
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


public class OBConversion {
  private long swigCPtr;
  protected boolean swigCMemOwn;

  protected OBConversion(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(OBConversion obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if(swigCPtr != 0 && swigCMemOwn) {
      swigCMemOwn = false;
      openbabelJNI.delete_OBConversion(swigCPtr);
    }
    swigCPtr = 0;
  }

  public OBConversion(SWIGTYPE_p_std__istream is, SWIGTYPE_p_std__ostream os) {
    this(openbabelJNI.new_OBConversion__SWIG_0(SWIGTYPE_p_std__istream.getCPtr(is), SWIGTYPE_p_std__ostream.getCPtr(os)), true);
  }

  public OBConversion(SWIGTYPE_p_std__istream is) {
    this(openbabelJNI.new_OBConversion__SWIG_1(SWIGTYPE_p_std__istream.getCPtr(is)), true);
  }

  public OBConversion() {
    this(openbabelJNI.new_OBConversion__SWIG_2(), true);
  }

  public OBConversion(OBConversion o) {
    this(openbabelJNI.new_OBConversion__SWIG_3(OBConversion.getCPtr(o), o), true);
  }

  public static int RegisterFormat(String ID, OBFormat pFormat, String MIME) {
    return openbabelJNI.OBConversion_RegisterFormat__SWIG_0(ID, OBFormat.getCPtr(pFormat), pFormat, MIME);
  }

  public static int RegisterFormat(String ID, OBFormat pFormat) {
    return openbabelJNI.OBConversion_RegisterFormat__SWIG_1(ID, OBFormat.getCPtr(pFormat), pFormat);
  }

  public static OBFormat FindFormat(String ID) {
    long cPtr = openbabelJNI.OBConversion_FindFormat(ID);
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public static OBFormat FormatFromExt(String filename) {
    long cPtr = openbabelJNI.OBConversion_FormatFromExt(filename);
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public static OBFormat FormatFromMIME(String MIME) {
    long cPtr = openbabelJNI.OBConversion_FormatFromMIME(MIME);
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public static boolean GetNextFormat(SWIGTYPE_p_OpenBabel__FMapType__iterator itr, SWIGTYPE_p_char str, OBFormat pFormat) {
    return openbabelJNI.OBConversion_GetNextFormat(SWIGTYPE_p_OpenBabel__FMapType__iterator.getCPtr(itr), SWIGTYPE_p_char.getCPtr(str), OBFormat.getCPtr(pFormat));
  }

  public static String Description() {
    return openbabelJNI.OBConversion_Description();
  }

  public SWIGTYPE_p_std__istream GetInStream() {
    long cPtr = openbabelJNI.OBConversion_GetInStream(swigCPtr, this);
    return (cPtr == 0) ? null : new SWIGTYPE_p_std__istream(cPtr, false);
  }

  public SWIGTYPE_p_std__ostream GetOutStream() {
    long cPtr = openbabelJNI.OBConversion_GetOutStream(swigCPtr, this);
    return (cPtr == 0) ? null : new SWIGTYPE_p_std__ostream(cPtr, false);
  }

  public void SetInStream(SWIGTYPE_p_std__istream pIn) {
    openbabelJNI.OBConversion_SetInStream(swigCPtr, this, SWIGTYPE_p_std__istream.getCPtr(pIn));
  }

  public void SetOutStream(SWIGTYPE_p_std__ostream pOut) {
    openbabelJNI.OBConversion_SetOutStream(swigCPtr, this, SWIGTYPE_p_std__ostream.getCPtr(pOut));
  }

  public boolean SetInAndOutFormats(String inID, String outID) {
    return openbabelJNI.OBConversion_SetInAndOutFormats__SWIG_0(swigCPtr, this, inID, outID);
  }

  public boolean SetInAndOutFormats(OBFormat pIn, OBFormat pOut) {
    return openbabelJNI.OBConversion_SetInAndOutFormats__SWIG_1(swigCPtr, this, OBFormat.getCPtr(pIn), pIn, OBFormat.getCPtr(pOut), pOut);
  }

  public boolean SetInFormat(String inID) {
    return openbabelJNI.OBConversion_SetInFormat__SWIG_0(swigCPtr, this, inID);
  }

  public boolean SetInFormat(OBFormat pIn) {
    return openbabelJNI.OBConversion_SetInFormat__SWIG_1(swigCPtr, this, OBFormat.getCPtr(pIn), pIn);
  }

  public boolean SetOutFormat(String outID) {
    return openbabelJNI.OBConversion_SetOutFormat__SWIG_0(swigCPtr, this, outID);
  }

  public boolean SetOutFormat(OBFormat pOut) {
    return openbabelJNI.OBConversion_SetOutFormat__SWIG_1(swigCPtr, this, OBFormat.getCPtr(pOut), pOut);
  }

  public OBFormat GetInFormat() {
    long cPtr = openbabelJNI.OBConversion_GetInFormat(swigCPtr, this);
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public OBFormat GetOutFormat() {
    long cPtr = openbabelJNI.OBConversion_GetOutFormat(swigCPtr, this);
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public String GetInFilename() {
    return openbabelJNI.OBConversion_GetInFilename(swigCPtr, this);
  }

  public SWIGTYPE_p_std__streampos GetInPos() {
    return new SWIGTYPE_p_std__streampos(openbabelJNI.OBConversion_GetInPos(swigCPtr, this), true);
  }

  public long GetInLen() {
    return openbabelJNI.OBConversion_GetInLen(swigCPtr, this);
  }

  public String GetTitle() {
    return openbabelJNI.OBConversion_GetTitle(swigCPtr, this);
  }

  public OBConversion GetAuxConv() {
    long cPtr = openbabelJNI.OBConversion_GetAuxConv(swigCPtr, this);
    return (cPtr == 0) ? null : new OBConversion(cPtr, false);
  }

  public void SetAuxConv(OBConversion pConv) {
    openbabelJNI.OBConversion_SetAuxConv(swigCPtr, this, OBConversion.getCPtr(pConv), pConv);
  }

  public String IsOption(String opt, OBConversion.Option_type opttyp) {
    return openbabelJNI.OBConversion_IsOption__SWIG_0(swigCPtr, this, opt, opttyp.swigValue());
  }

  public String IsOption(String opt) {
    return openbabelJNI.OBConversion_IsOption__SWIG_1(swigCPtr, this, opt);
  }

  public SWIGTYPE_p_std__mapTstd__string_std__string_t GetOptions(OBConversion.Option_type opttyp) {
    long cPtr = openbabelJNI.OBConversion_GetOptions(swigCPtr, this, opttyp.swigValue());
    return (cPtr == 0) ? null : new SWIGTYPE_p_std__mapTstd__string_std__string_t(cPtr, false);
  }

  public void AddOption(String opt, OBConversion.Option_type opttyp, String txt) {
    openbabelJNI.OBConversion_AddOption__SWIG_0(swigCPtr, this, opt, opttyp.swigValue(), txt);
  }

  public void AddOption(String opt, OBConversion.Option_type opttyp) {
    openbabelJNI.OBConversion_AddOption__SWIG_1(swigCPtr, this, opt, opttyp.swigValue());
  }

  public boolean RemoveOption(String opt, OBConversion.Option_type optype) {
    return openbabelJNI.OBConversion_RemoveOption(swigCPtr, this, opt, optype.swigValue());
  }

  public void SetOptions(String options, OBConversion.Option_type opttyp) {
    openbabelJNI.OBConversion_SetOptions(swigCPtr, this, options, opttyp.swigValue());
  }

  public static void RegisterOptionParam(String name, OBFormat pFormat, int numberParams, OBConversion.Option_type typ) {
    openbabelJNI.OBConversion_RegisterOptionParam__SWIG_0(name, OBFormat.getCPtr(pFormat), pFormat, numberParams, typ.swigValue());
  }

  public static void RegisterOptionParam(String name, OBFormat pFormat, int numberParams) {
    openbabelJNI.OBConversion_RegisterOptionParam__SWIG_1(name, OBFormat.getCPtr(pFormat), pFormat, numberParams);
  }

  public static void RegisterOptionParam(String name, OBFormat pFormat) {
    openbabelJNI.OBConversion_RegisterOptionParam__SWIG_2(name, OBFormat.getCPtr(pFormat), pFormat);
  }

  public static int GetOptionParams(String name, OBConversion.Option_type typ) {
    return openbabelJNI.OBConversion_GetOptionParams(name, typ.swigValue());
  }

  public vectorString GetSupportedInputFormat() {
    return new vectorString(openbabelJNI.OBConversion_GetSupportedInputFormat(swigCPtr, this), true);
  }

  public vectorString GetSupportedOutputFormat() {
    return new vectorString(openbabelJNI.OBConversion_GetSupportedOutputFormat(swigCPtr, this), true);
  }

  public int Convert(SWIGTYPE_p_std__istream is, SWIGTYPE_p_std__ostream os) {
    return openbabelJNI.OBConversion_Convert__SWIG_0(swigCPtr, this, SWIGTYPE_p_std__istream.getCPtr(is), SWIGTYPE_p_std__ostream.getCPtr(os));
  }

  public int Convert() {
    return openbabelJNI.OBConversion_Convert__SWIG_1(swigCPtr, this);
  }

  public int FullConvert(vectorString FileList, SWIGTYPE_p_std__string OutputFileName, vectorString OutputFileList) {
    return openbabelJNI.OBConversion_FullConvert(swigCPtr, this, vectorString.getCPtr(FileList), FileList, SWIGTYPE_p_std__string.getCPtr(OutputFileName), vectorString.getCPtr(OutputFileList), OutputFileList);
  }

  public boolean AddChemObject(OBBase pOb) {
    return openbabelJNI.OBConversion_AddChemObject(swigCPtr, this, OBBase.getCPtr(pOb), pOb);
  }

  public OBBase GetChemObject() {
    long cPtr = openbabelJNI.OBConversion_GetChemObject(swigCPtr, this);
    return (cPtr == 0) ? null : new OBBase(cPtr, false);
  }

  public boolean IsLast() {
    return openbabelJNI.OBConversion_IsLast(swigCPtr, this);
  }

  public boolean IsFirstInput() {
    return openbabelJNI.OBConversion_IsFirstInput(swigCPtr, this);
  }

  public int GetOutputIndex() {
    return openbabelJNI.OBConversion_GetOutputIndex(swigCPtr, this);
  }

  public void SetOutputIndex(int indx) {
    openbabelJNI.OBConversion_SetOutputIndex(swigCPtr, this, indx);
  }

  public void SetMoreFilesToCome() {
    openbabelJNI.OBConversion_SetMoreFilesToCome(swigCPtr, this);
  }

  public void SetOneObjectOnly(boolean b) {
    openbabelJNI.OBConversion_SetOneObjectOnly__SWIG_0(swigCPtr, this, b);
  }

  public void SetOneObjectOnly() {
    openbabelJNI.OBConversion_SetOneObjectOnly__SWIG_1(swigCPtr, this);
  }

  public void SetLast(boolean b) {
    openbabelJNI.OBConversion_SetLast(swigCPtr, this, b);
  }

  public static OBFormat GetDefaultFormat() {
    long cPtr = openbabelJNI.OBConversion_GetDefaultFormat();
    return (cPtr == 0) ? null : new OBFormat(cPtr, false);
  }

  public boolean Write(OBBase pOb, SWIGTYPE_p_std__ostream pout) {
    return openbabelJNI.OBConversion_Write__SWIG_0(swigCPtr, this, OBBase.getCPtr(pOb), pOb, SWIGTYPE_p_std__ostream.getCPtr(pout));
  }

  public boolean Write(OBBase pOb) {
    return openbabelJNI.OBConversion_Write__SWIG_1(swigCPtr, this, OBBase.getCPtr(pOb), pOb);
  }

  public String WriteString(OBBase pOb, boolean trimWhitespace) {
    return openbabelJNI.OBConversion_WriteString__SWIG_0(swigCPtr, this, OBBase.getCPtr(pOb), pOb, trimWhitespace);
  }

  public String WriteString(OBBase pOb) {
    return openbabelJNI.OBConversion_WriteString__SWIG_1(swigCPtr, this, OBBase.getCPtr(pOb), pOb);
  }

  public boolean WriteFile(OBBase pOb, String filePath) {
    return openbabelJNI.OBConversion_WriteFile(swigCPtr, this, OBBase.getCPtr(pOb), pOb, filePath);
  }

  public void CloseOutFile() {
    openbabelJNI.OBConversion_CloseOutFile(swigCPtr, this);
  }

  public boolean Read(OBBase pOb, SWIGTYPE_p_std__istream pin) {
    return openbabelJNI.OBConversion_Read__SWIG_0(swigCPtr, this, OBBase.getCPtr(pOb), pOb, SWIGTYPE_p_std__istream.getCPtr(pin));
  }

  public boolean Read(OBBase pOb) {
    return openbabelJNI.OBConversion_Read__SWIG_1(swigCPtr, this, OBBase.getCPtr(pOb), pOb);
  }

  public boolean ReadString(OBBase pOb, String input) {
    return openbabelJNI.OBConversion_ReadString(swigCPtr, this, OBBase.getCPtr(pOb), pOb, input);
  }

  public boolean ReadFile(OBBase pOb, String filePath) {
    return openbabelJNI.OBConversion_ReadFile(swigCPtr, this, OBBase.getCPtr(pOb), pOb, filePath);
  }

  public final static class Option_type {
    public final static Option_type INOPTIONS = new Option_type("INOPTIONS");
    public final static Option_type OUTOPTIONS = new Option_type("OUTOPTIONS");
    public final static Option_type GENOPTIONS = new Option_type("GENOPTIONS");

    public final int swigValue() {
      return swigValue;
    }

    public String toString() {
      return swigName;
    }

    public static Option_type swigToEnum(int swigValue) {
      if (swigValue < swigValues.length && swigValue >= 0 && swigValues[swigValue].swigValue == swigValue)
        return swigValues[swigValue];
      for (int i = 0; i < swigValues.length; i++)
        if (swigValues[i].swigValue == swigValue)
          return swigValues[i];
      throw new IllegalArgumentException("No enum " + Option_type.class + " with value " + swigValue);
    }

    private Option_type(String swigName) {
      this.swigName = swigName;
      this.swigValue = swigNext++;
    }

    private Option_type(String swigName, int swigValue) {
      this.swigName = swigName;
      this.swigValue = swigValue;
      swigNext = swigValue+1;
    }

    private Option_type(String swigName, Option_type swigEnum) {
      this.swigName = swigName;
      this.swigValue = swigEnum.swigValue;
      swigNext = this.swigValue+1;
    }

    private static Option_type[] swigValues = { INOPTIONS, OUTOPTIONS, GENOPTIONS };
    private static int swigNext = 0;
    private final int swigValue;
    private final String swigName;
  }

}
