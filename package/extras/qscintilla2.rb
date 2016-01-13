class Qscintilla2 < Formula
  desc "Port to Qt of the Scintilla editing component"
  homepage "https://www.riverbankcomputing.com/software/qscintilla/intro"
  url "https://downloads.sf.net/project/pyqt/QScintilla2/QScintilla-2.8.4/QScintilla-gpl-2.8.4.tar.gz"
  sha256 "9b7b2d7440cc39736bbe937b853506b3bd218af3b79095d4f710cccb0fabe80f"

  depends_on :python3
  depends_on "pyqt5"

  def install
    cd "Qt4Qt5" do
      qmake = "#{Formula["qt5"].bin}/qmake"
      system qmake, "qscintilla.pro"
      system "make"
      system "make", "install"
    end

    cd "Python" do
      configure_args = [
        "--verbose",
        "--pyqt=PyQt5",
        "--qmake=#{Formula["qt5"].bin}/qmake",
        "--qsci-incdir=#{Formula["qt5"].include}",
        "--qsci-libdir=#{Formula["qt5"].lib}",
        "--sip-incdir=#{Formula["sip"].include}",
        "--pyqt-sipdir=#{Formula["pyqt5"].share}/sip/Qt5",
        "--destdir=#{lib}/python3.5/site-packages/PyQt5"
      ]
      system "python3", "configure.py", *configure_args
      system "make"
      system "make", "install"
      system "make", "clean"
    end
  end

  test do
    Pathname("test.py").write <<-EOS.undent
      import PyQt5.Qsci
      assert("QsciLexer" in dir(PyQt5.Qsci))
    EOS
    Language::Python.each_python(build) do |python, _version|
      system "python3", "test.py"
    end
  end
end
