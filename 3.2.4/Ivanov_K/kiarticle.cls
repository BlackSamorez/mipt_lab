\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{kiarticle}
\ProcessOptions

\LoadClass
    [12pt, a4paper, oneside, final]{article}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                 Математика                                  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{mathtext}
\RequirePackage{mathtools}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage[all,warning]
               {onlyamsmath}
    \AtBeginDocument{\catcode`\$=3}
\RequirePackage{cancel}
\RequirePackage{icomma}
\RequirePackage{mathrsfs}
\RequirePackage{bigints}
\RequirePackage{mathrsfs}
%\RequirePackage{physics}
\RequirePackage{indentfirst}
\mathtoolsset{showonlyrefs=true} % Показывать номера только у тех формул, на которые есть \eqref{} в тексте.


\RequirePackage{udef}
\RequirePackage{iunits}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Формат документа                               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[T2A,OT1]           {fontenc}
\RequirePackage[utf8]              {inputenc}
\RequirePackage[english, russian]  {babel}
\RequirePackage[ left     = 1.5cm,
                 right    = 1.5cm,
                 top      = 2.0cm,
                 bottom   = 1.25cm,
                 includefoot,
                 footskip = 1.25cm ]{geometry}
\setlength    {\parskip}        { .5em plus .15em minus .08em }
%\setlength    {\parindent}      { .0em }
\renewcommand {\baselinestretch}{ 1.07 }


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                  Графика                                    %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{wrapfig}
\RequirePackage{color}
\RequirePackage{tikz}
\RequirePackage{pgfplots}
    \pgfplotsset{compat=newest}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                        Нумерация, заголовки и подписи                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{fancyref}
\RequirePackage{fancyhdr}

\RequirePackage{secdot}
\RequirePackage{caption}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Таблицы и списки                               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{enumitem}
    \setlist{leftmargin =   1cm,
             topsep     =  .0\parskip,
             itemsep    = -.0\parskip,
             resume
            }
\RequirePackage{booktabs}
\RequirePackage{array}
    \renewcommand{\arraystretch}{ 1.20 }
